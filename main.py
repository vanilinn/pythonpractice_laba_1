from datetime import datetime  

from courier import Courier
from item import Item
from provider import Provider
from store import Store
import utils
from storekeeper import Storekeeper
from user import User

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
store1.send_request([item1, item2, item4, item5])
store2.send_request([item1, item2, item3, item4])

# Создание объекта класса User (пользователь)
user1 = User('Вася', (10, 10))
user2 = User('Петя', (20, 20))

# Создание заказов пользователя
order1 = user1.make_order([item1, item2, item3, item5])
order2 = user1.make_order([item1, item2])
order3 = user2.make_order([item1, item5])

# Создание объектов класса Courier (курьеры) и назначение им смен
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

# Установка времени отправки заказов
order1_time = datetime(2022, 1, 1, 10, 1, 0)
order2_time = datetime(2022, 1, 1, 10, 0, 0)
order3_time = datetime(2022, 1, 1, 10, 2, 0)
order1.time_start = order1_time
order2.time_start = order2_time
order3.time_start = order3_time

# Определение самого быстрого магазина для выполнения заказов и назначение заказов этим магазинам
utils.send_order_to_fastest_store(stores, order2)
utils.send_order_to_fastest_store(stores, order1)
utils.send_order_to_fastest_store(stores, order3)
