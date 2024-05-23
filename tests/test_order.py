import pytest
import allure


@allure.feature('Создание и выгрузка заказов')
@pytest.mark.usefixtures('create_order')
class TestOrder:
    @allure.title('Можно указать один из цветов — BLACK или GREY, ответ содержит "track"')
    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'], ])
    def test_create_order_successful(self, color):
        self.order_with.payload["color"] = color
        response = self.order_with.post_create_order(data=self.order_with.payload)
        assert "track" in response

    @allure.title('Можно не указывать цвет, ответ содержит "track"')
    def test_order_no_color(self):
        self.order_with.payload["color"] = None
        response = self.order_with.post_create_order(data=self.order_with.payload)
        assert "track" in response

    @allure.title('Тело ответа возвращается список заказов')
    def test_get_order_list(self):
        response = self.order_with.list_of_orders()
        assert "orders" in response
