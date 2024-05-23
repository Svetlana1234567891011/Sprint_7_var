import json
import random
import string

import requests
import allure


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


class MainRequests:
    host = 'https://qa-scooter.praktikum-services.ru'
    courier_create = '/api/v1/courier'
    courier_login = '/api/v1/courier/login'

    def post_request_transform_and_check(self, url, data):
        response = requests.post(url=url, json=data)
        if response.headers.get('Content-Type') and 'application/json' in response.headers['Content-Type']:
            # if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def delete_request_transform_and_check(self, url, data):
        response = requests.delete(url=url, data=data)
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def get_request_transform_and_check(self, url):
        response = requests.get(url=url)
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def put_request_transform_and_check(self, url, data):
        response = requests.put(url=url, data=data)
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def post_request_transform_and_check_ord(self, url, data):  # проверяем код ответа
        response = requests.post(url=url, data=data)  # кладем код ответа в переменную response
        if 'application/json' in response.headers['Content-Type']:  # Функция exec_post_request_and_check проверяет
            return response.json()  # если тип содержимого ответа - JSON, возвращает его в формате словаря, иначе возвращает текст ответа.
        else:
            return response.text


class CourierRequests(MainRequests):
    def __init__(self):
        self.payload = None
        self.is_deleted = False

    courier_create = '/api/v1/courier'
    courier_login = '/api/v1/courier/login'

    @allure.step('Создаем курьера, отправив запрос POST')
    def post_create_courier(self, data=None):
        url = f"{self.host}{self.courier_create}"
        return self.post_request_transform_and_check(url, data=data)

    @allure.step('Логиним курьера, отправив запрос POST')
    def post_login_courier(self, data=None):
        url = f"{self.host}{self.courier_login}"
        return self.post_request_transform_and_check(url, data=data)

    @allure.step('Удаляем курьера, отправив запрос DELETE.')
    def delete_courier(self, courier_id=None):
        url = f"{self.host}{self.courier_create}/{courier_id}"
        delete_payload = {"id": courier_id}
        return self.delete_request_transform_and_check(url, data=delete_payload)


class OrderRequests(MainRequests):
    order_point = '/api/v1/orders'

    def __init__(self, payload):
        self.payload = payload

    @allure.step('Создаем заказ, отправив запрос POST.')
    def post_create_order(self, data=None):
        url = f"{self.host}{self.order_point}"
        return self.post_request_transform_and_check_ord(url, data=json.dumps(data))

    @allure.step('Отправляем get, получаем список заказов')
    def list_of_orders(self):
        url = f"{self.host}{self.order_point}"
        return self.get_request_transform_and_check(url)
