import pytest
import allure
from utils.special_request import CourierRequests, generate_random_string


randoms_string = generate_random_string(10)


@pytest.mark.usefixtures("create_payload")
@allure.feature('Создание курьера')
class TestCreateCourier:

    @allure.title('Можно создать курьера со случайным логином')
    @pytest.mark.parametrize('login_v, password_v, firstname_v',
                             [
                                 (randoms_string, randoms_string, randoms_string),
                             ])
    def test_all_the_fields_are_required(self, login_v, password_v, firstname_v):
        payload = {
            "login": login_v,
            "password": password_v,
            "firstName": firstname_v
        }

        response = CourierRequests().post_create_courier(data=payload)
        assert response['ok']

    # @allure.title('Нельзя создать двух курьеров с одинаковыми логинами')
    # def test_cant_create_courier_dupes(self, courier_with_payload):
    #     #courier_with_payload.post_create_courier(data=courier_with_payload.payload)  # отправляем данные
    #
    #     response_dupe = CourierRequests().post_create_courier(data=self.payload,
    #                                                           status=409)  # отправляем данные повторно
    #     assert response_dupe["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title('Нельзя создать двух курьеров с одинаковыми логинами')
    def test_cant_create_courier_dupes(self, courier_with_payload):
        response_dupe = courier_with_payload.post_create_courier(data=courier_with_payload.payload)  # отправляем данные  # отправляем данные повторно
        assert response_dupe["message"] == "Этот логин уже используется. Попробуйте другой."

    @pytest.mark.parametrize('login_v, password_v, firstname_v',
                             [
                                 (None, randoms_string, randoms_string),
                                 (None, randoms_string, None),
                                 (randoms_string, None, None),
                                 (None, None, randoms_string),

                             ])
    @allure.title('Для создания курьера необходимо задать все обязательные поля (логин, пароль)')
    def test_all_the_fields_are_required(self, login_v, password_v, firstname_v):
        payload = {
            "login": login_v,
            "password": password_v,
            "firstName": firstname_v
        }

        response = CourierRequests().post_create_courier(data=payload)
        assert response["message"] == "Недостаточно данных для создания учетной записи"
