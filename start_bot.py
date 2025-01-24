import telebot
from telebot import types

from IMEI_API import Imei_Api_Info
from config import TELEGRAM_TOKEN, white_list_users

bot = telebot.TeleBot(TELEGRAM_TOKEN)

markup = types.ReplyKeyboardMarkup()
btn1 = types.KeyboardButton(text="Информация по IMEI")
btn2 = types.KeyboardButton(text="Узнать баланс")
btn3 = types.KeyboardButton(text="Посмотреть все услуги сервиса")
markup.row(btn1, btn2)
markup.row(btn3)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in white_list_users:
        bot.send_message(message.chat.id,
                     f"Привет, {message.from_user.first_name}! Это IMEI_bot.\U0001F916"
                         )
        user_autorization(message)
    else:
        bot.send_message(message.chat.id,
                     "В доступе отказано!\U0001F480"
                     )

def user_autorization(message):
    bot.send_message(message.chat.id,
                     "Тебе необходимо авторизоваться, чтобы получить доступ к сервису")
    bot.send_message(message.chat.id,
                     "Введи API токен")
    bot.register_next_step_handler(message, on_token_entered)


def on_token_entered(message):
    token = message.text
    service = Imei_Api_Info(token)

    if 'error' not in service.authorization():
        bot.send_message(message.chat.id,
                     "API токен успешно сохранен. Теперь ты можешь получать данные с сервиса", reply_markup=markup)
        menu(message, service)
    else:
        bot.send_message(message.chat.id,
                     "Ошибка авторизации. Проверьте правильность введенного API токена")
        user_autorization(message)


def menu(message, service):
    bot.send_message(message.chat.id,
                     "Выбери услугу:", reply_markup=markup)
    bot.send_message(message.chat.id,
                     f"Информация о IMEI\nУзнать баланс\nПосмотреть все услуги сервиса")
    bot.register_next_step_handler(message, service_list, service)


def service_list(message, service):
    service_name = message.text

    if service_name == "Информация по IMEI":
        bot.send_message(message.chat.id,
                         f"Введи IMEI")
        bot.register_next_step_handler(message, imei_info, service)

    elif service_name == "Узнать баланс":
        bot.send_message(message.chat.id,
                         f"Твой текущий баланс: {service.get_balance()}")
        menu(message, service)

    elif service_name == "Посмотреть все услуги сервиса":
        service_list = service.get_service_list()
        for i in service_list:
            bot.send_message(message.chat.id,f"Услуга #{i['id']}. {i['title']}, цена: {i['price']}.")
        menu(message, service)

    else:
        bot.send_message(message.chat.id,
                     "Неправильный выбор сервиса. Попробуйте еще раз")
        menu(message, service)


def imei_info(message, service):
    """Выполняет валидацию IMEI и возвращает о нем информацию"""

    imei = message.text
    if imei.isdigit() and len(imei) == 15:
        info = service.get_imei_info(imei)

        if 'error' not in info:
            bot.send_message(message.chat.id,
                     f"Получены следующие данные:\n{info[0]['properties']}")
            menu(message, service)
        else:
            bot.send_message(message.chat.id,
                     "Ошибка получения информации о IMEI. Попробуйте повторить попытку")
            imei_info(message, service)
    else:
        bot.send_message(message.chat.id,
                     "Неправильный ввод IMEI. Введите 15-значный номер")
        bot.register_next_step_handler(message, imei_info, service)



bot.polling(none_stop=True)
