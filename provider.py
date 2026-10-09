from item import Item
from calculations import pick_items
import console_view


class Provider:  # поставщик
    def __init__(self, prov_id: int | str, stock: list[Item]):
        self.__provider_id = prov_id
        self.__stock = stock
        self.__current_stock = self.__stock.copy()

    def send_order(self, order: list[Item]):
        # Метод для отправки заказа складу
        remaining, sent, _missing = pick_items(self.__current_stock, order)
        # Раньше остаток и полный ассортимент могли быть одним списком,
        # и удаление меняло оба. Теперь сохраняем новый список, не трогая старый.
        if self.__current_stock is self.__stock:
            self.__stock = remaining
        self.__current_stock = remaining
        return sent

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
