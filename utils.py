import math
from datetime import timedelta
import random


def calculate_order_time(store, order):
    # Функция для расчета времени обработки заказа
    store_coords = store.coords  # Координаты магазина
    order_coords = order.user_coords  # Координаты пользователя
    dist = round(math.sqrt((store_coords[0] - order_coords[0]) ** 2 + (
                store_coords[1] - order_coords[1]) ** 2))  # Расстояние между магазином и пользователем
    store_stock = store.stock.copy()  # Копия ассортимента магазина
    time_to_assemble = 0  # Время на сборку заказа
    for item in order.items:
        if item in store_stock:
            store_stock.remove(item)
            time_to_assemble += 45  # Время на сборку каждого товара
    if time_to_assemble == 0:
        return math.inf
    total_time = dist * 30 + time_to_assemble + 120  # Общее время доставки заказа
    if len(store.list_of_couriers) == 0 or len(store.list_of_storekeepers) == 0:
        # Если нет свободных курьеров или кладовщиков, возвращаем бесконечность
        return math.inf
    is_available_storekeeper = False
    is_available_courier = False
    for storekeeper in store.list_of_storekeepers:
        time_left = (storekeeper.get_job_end() - order.time_start).total_seconds()
        # Курьер должен быть свободен, успеть закончить предыдущий заказ и знать, что успеет этот
        if storekeeper.get_status() == 'свободен' and time_left >= time_to_assemble and storekeeper.get_job_start() <= order.time_start:
            is_available_storekeeper = True
            break
    for courier in store.list_of_couriers:
        time_left = (courier.get_job_end() - order.time_start).total_seconds()
        # Аналогично для курьера
        if courier.get_status() == 'свободен' and time_left >= total_time and courier.get_job_start() <= order.time_start + timedelta(
                seconds=time_to_assemble):
            is_available_courier = True
            break
    if not is_available_storekeeper or not is_available_courier:
        return math.inf  # Если нет доступных кладовщиков или курьеров, возвращаем бесконечность
    return total_time  # Возвращаем общее время доставки заказа


def get_fastest_store(stores: list, order):
    # Функция для определения самого быстрого магазина для обработки заказа
    min_time = math.inf  # Изначально минимальное время устанавливаем как бесконечность
    fastest_store = None
    for store in stores:
        if calculate_order_time(store, order) <= min_time:
            min_time = calculate_order_time(store, order)
            fastest_store = store
    if min_time == math.inf:
        print('Нет свободных магазинов')
        return None  # Если нет доступных магазинов, возвращаем None
    if fastest_store is not None:
        print(f'Быстрее всего заказ {order.id} будет обработан магазином {fastest_store.id_of_store}')
        print(f'Время обработки: {min_time} секунд')
        return fastest_store
    return None  # Если не удалось определить самый быстрый магазин, возвращаем None


def is_courier_a_schoolboy():
    number = random.randint(1, 10)
    if number == 1:
        return True
    return False


def send_order_to_fastest_store(stores, order):
    fastest_store = get_fastest_store(stores, order)
    if fastest_store is not None:
        fastest_store.take_order(order)
