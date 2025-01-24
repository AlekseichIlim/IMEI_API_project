import json

import requests


class Imei_Api_Info:
    """Класс для получения информации об IMEI через API"""

    def __init__(self, token):
        self.token = token
        self.__url = 'https://api.imeicheck.net/v1'
        self.__headers = {'Authorization': f'Bearer {self.token}',
                          'Content-Type': 'application/json'
                          }
        self.authorization()

    def authorization(self):
        """Авторизация пользователя по API токену. При успешной авторизации возвращает информацию о балансе"""

        response = requests.get(self.__url + '/account', headers=self.__headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Request failed', 'status_code': response.status_code, 'detail': response.reason}

    def get_balance(self):
        """Получение текущего баланса пользователя"""

        info = self.authorization()
        if 'error' not in info:
            return info['balance']
        else:
            return info

    def get_service_list(self):
        """Получение списка доступных услуг"""

        response = requests.get(self.__url + '/services', headers=self.__headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Request failed', 'status_code': response.status_code, 'detail': response.reason}

    def get_imei_info(self, imei):
        """Получение информации об IMEI через API"""

        body = json.dumps({
            "imei": imei,
            "serviceId": 6
        })

        response = requests.get(self.__url + '/checks', headers=self.__headers, data=body)

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Request failed', 'status_code': response.status_code, 'detail': response.reason}
