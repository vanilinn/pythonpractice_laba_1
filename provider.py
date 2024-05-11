from item import Item
import console_view


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
        def block(title, goods):
            if not goods:
                body = "    пусто"
            else:
                body = "\n".join(f"    {console_view.item_line(el)}" for el in goods)
            return f"  {title}:\n{body}"

        return (
            f"Поставщик {self.__provider_id}\n"
            f"{block('сейчас может отгрузить', self.__current_stock)}\n"
            f"{block('полный ассортимент', self.__stock)}"
        )
