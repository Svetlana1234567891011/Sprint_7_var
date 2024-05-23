import pytest
from conftest import create_payload
from utils.special_request import CourierRequests, generate_random_string
import allure

randoms_string = generate_random_string(10)


@allure.feature('Проверка авторизации курьера, успешный запрос возвращает id')
class TestLogin:
    @allure.title('Курьер может авторизоваться с существующей учетной записью')
    def test_courier_can_login(self, courier_with_payload):
        response = courier_with_payload.post_login_courier(data=courier_with_payload.payload)
        assert response['id']

    @pytest.mark.parametrize("change_value",
                             ["login"]
                             )
    @allure.title('Курьер с отсутствующим логином не может залогиниться')
    def test_courier_cannot_login(self, courier_with_payload, change_value):
        courier_with_payload.payload[change_value] = None  # Удаляем логин
        response = courier_with_payload.post_login_courier(data=courier_with_payload.payload)
        assert response['message'] == 'Недостаточно данных для входа'

    @pytest.mark.parametrize("change_value",
                             ["login",
                              "password"]
                             )
    @allure.title('Система вернёт ошибку, если неправильно указать логин или пароль')
    def test_courier_cannot_login_due_wrong_input(self, change_value, create_payload):
        CourierRequests().post_create_courier(data=create_payload)
        create_payload[change_value] = randoms_string
        response = CourierRequests().post_login_courier(data=create_payload)
        assert response['message'] == 'Учетная запись не найдена'

    @pytest.mark.parametrize("change_value",
                             ["login",
                              "password"]
                             )
    @allure.title('Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    def test_courier_cant_login_for_deleted_account(self, change_value, courier_with_payload):
        courier_with_payload.payload[change_value] = randoms_string
        response = CourierRequests().post_login_courier(data=courier_with_payload.payload)
        assert response.get('message') == 'Учетная запись не найдена'

    @allure.title('Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    def test_courier_cant_login_for_deleted_account(self, courier_with_payload):
        response = courier_with_payload.post_login_courier(data=courier_with_payload.payload)
        courier_id = response["id"]
        courier_with_payload.delete_courier(courier_id=courier_id)
        response = courier_with_payload.post_login_courier(data=courier_with_payload.payload)

        assert response.get('message') == 'Учетная запись не найдена'
