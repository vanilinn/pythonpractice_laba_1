from datetime import datetime
import uuid

from courier import Courier
from item import Item
from order import make_order
from provider import Provider
from store import Store
import utils
from storekeeper import Storekeeper
from user import User
import console_view

console_view.print_intro()

# Создание объектов класса Item (товары)
item1 = Item('печенье', 100, 1, 1)
item2 = Item('хлеб', 20, 1, 1)
item3 = Item('молоко', 30, 1, 1)
item4 = Item('масло', 50, 1, 1)
item5 = Item('пиво', 60, 2, 1)

# Создание объектов класса Provider (поставщики товаров)
zavod1 = Provider(1, [item1, item2, item3, item4])
pivsavod = Provider(2, [item5])

# Создание объектов класса Store (магазины)
schedule1 = [datetime(2022, 1, 1, 9, 0, 0), datetime(2022, 1, 1, 21, 0, 0)]
schedule2 = [datetime(2022, 1, 1, 8, 0, 0), datetime(2022, 1, 1, 20, 0, 0)]
store1 = Store(1, (1, 1), [], [zavod1, pivsavod], schedule1)
store2 = Store(2, (5, 5), [], [zavod1, pivsavod], schedule2)

# Отправка запросов на поставку товаров в магазины
console_view.heading("Поставка")
store1.send_request([item1, item2, item4, item5], reason="старт")
store2.send_request([item1, item2, item3, item4], reason="старт")

# Создание объекта класса User (пользователь)
console_view.heading("Покупатели")
user1 = User('Вася', (10, 10))
user2 = User('Петя', (20, 20))
console_view.print_user(user1)
console_view.print_user(user2)

# Создание объектов класса Courier (курьеры) и назначение им смен
console_view.heading("Смены")
courier1 = Courier(1, 'Курьер1')
courier2 = Courier(2, 'Курьер2')
courier1.get_shift(store1, 10)
courier2.get_shift(store2, 10)

# Создание объектов класса Storekeeper (кладовщики) и назначение им смен
storekeeper1 = Storekeeper(1, 'Кладовщик1')
storekeeper2 = Storekeeper(2, 'Кладовщик2')
storekeeper1.get_shift(store1, 10)
storekeeper2.get_shift(store2, 10)

# Создание списка магазинов
stores = [store1, store2]

# Создание заказов: номер и время задаёт сценарий, а не сам объект пользователя
order1_time = datetime(2022, 1, 1, 10, 1, 0)
order2_time = datetime(2022, 1, 1, 10, 0, 0)
order3_time = datetime(2022, 1, 1, 10, 2, 0)
order1 = make_order(uuid.uuid4().hex, [item1, item2, item3, item5], order1_time, user1.id, user1.coords)
order2 = make_order(uuid.uuid4().hex, [item1, item2], order2_time, user1.id, user1.coords)
order3 = make_order(uuid.uuid4().hex, [item1, item5], order3_time, user2.id, user2.coords)
console_view.heading("Заказы")
console_view.print_order_created(user1, order1)
console_view.print_order_created(user1, order2)
console_view.print_order_created(user2, order3)

# Определение самого быстрого магазина для выполнения заказов и назначение заказов этим магазинам
utils.send_order_to_fastest_store(stores, order2)
utils.send_order_to_fastest_store(stores, order1)
utils.send_order_to_fastest_store(stores, order3)

console_view.print_session_report(
    stores,
    [order1, order2, order3],
    [user1, user2],
    [courier1, courier2],
    [storekeeper1, storekeeper2],
)
