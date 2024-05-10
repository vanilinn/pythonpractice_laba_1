from item import Item


class Provider:  # поставщик
    def __init__(self, prov_id: int | str, stock: list[Item]):
        self.__provider_id = prov_id
        self.__stock = stock
        self.__current_stock = self.__stock.copy()

    def send_order(self, order: list[Item]):
        # Метод для отправки заказа складу
        result = []
        for elem in order:
            if elem in self.__current_stock:
                result.append(elem)
                self.__current_stock.remove(elem)
        return result

    def update_stocks(self):
        # Метод для обновления запасов товаров на складе
        self.__current_stock = self.__stock

    def __str__(self):
        return f'{[f"Товар {el.title} стоимостью {el.cost} из магазина {el.store_id} от поставщика {el.provider_id}" for el in self.__current_stock]} / {[f"Товар {elem.title} стоимостью {elem.cost} из магазина {elem.store_id} от поставщика {elem.provider_id}" for elem in self.__stock]}'
