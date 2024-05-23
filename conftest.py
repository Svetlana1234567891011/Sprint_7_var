import pytest
import allure
from utils.special_request import CourierRequests, OrderRequests
from utils.special_request import CourierRequests
import random
import string

import string
import random
import pytest
import allure


@pytest.fixture(scope='class')
@allure.step('Создаем случайное число')
def generate_random_string_fix():
    def _generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string  # Возвращаем сгенерированную строку

    return _generate_random_string


@pytest.fixture(scope='class')
@allure.step('Создаем случайное число')
def generate_random_string_10(generate_random_string_fix):
    randoms_string = generate_random_string_fix(10)
    return randoms_string
    # request.cls.randomise_string = generate_random_string(10)


@allure.step('payload для пользователя')
@pytest.fixture
def create_payload(generate_random_string_10):
    login = generate_random_string_10
    password = generate_random_string_10
    first_name = generate_random_string_10

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    return payload


@pytest.fixture(scope='class')
@allure.step('payload заказа')
def create_order_payload(request, generate_random_string_10):
    payload = {"firstName": generate_random_string_10, "lastName": generate_random_string_10,
               "address": generate_random_string_10, "metroStation": 555, "phone": generate_random_string_10,
               "rentTime": 10,
               "deliveryDate": "2024-02-05",
               "comment": generate_random_string_10}
    # return payload
    return payload


@pytest.fixture(scope='class')
@allure.step('payload заказа')
def create_order(create_order_payload, request):
    order_with = OrderRequests(payload=create_order_payload)
    request.cls.order_with = order_with


created_couriers_list = []


@pytest.fixture(scope='function', autouse=True)
def courier_with_payload(create_payload):
    courier_requests = CourierRequests()
    # Создаем курьера
    payload = create_payload
    courier_requests.payload = payload  # Добавляем payload в объект
    courier_requests.post_create_courier(data=payload)
    created_couriers_list.append(courier_requests)

    return courier_requests


@pytest.fixture(scope='function', autouse=True)
def cleanup_couriers(courier_with_payload):
    yield  # Ничего не делаем до окончания теста

    try:
        response = courier_with_payload.post_login_courier(data=courier_with_payload.payload)
        courier_id = response.get("id")
        if courier_id:
            courier_with_payload.delete_courier(courier_id=courier_id)
    except Exception as e:
        # Если возникает ошибка при логине, просто пропускаем удаление
        print(f"Не удалось залогинить курьера для удаления: {e}")
