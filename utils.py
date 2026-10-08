import math
from datetime import timedelta
import random

from calculations import assemble_seconds, deliver_seconds
import console_view


def _names(titles):
    return ", ".join(titles)


def _keeper_problem(store, order, time_to_assemble):
    problems = []
    for storekeeper in store.list_of_storekeepers:
        time_left = (storekeeper.get_job_end() - order.time_start).total_seconds()
        name = storekeeper.get_name()
        if storekeeper.get_status() != 'свободен':
            problems.append(f"{name} занят ({storekeeper.get_status()})")
            continue
        if storekeeper.get_job_start() > order.time_start:
            free_at = console_view.format_clock(storekeeper.get_job_start())
            problems.append(f"{name} свободен только с {free_at}")
            continue
        if time_left < time_to_assemble:
            problems.append(f"{name} не успевает собрать до конца смены")
            continue
        return None
    if problems:
        return "; ".join(problems)
    return "нет свободного кладовщика"


def _courier_problem(store, order, time_to_assemble, total_time):
    problems = []
    for courier in store.list_of_couriers:
        time_left = (courier.get_job_end() - order.time_start).total_seconds()
        name = courier.get_name()
        if courier.get_status() != 'свободен':
            problems.append(f"{name} занят ({courier.get_status()})")
            continue
        if time_left < total_time:
            problems.append(f"{name} не успевает доставить до конца смены")
            continue
        if courier.get_job_start() > order.time_start + timedelta(seconds=time_to_assemble):
            free_at = console_view.format_clock(courier.get_job_start())
            problems.append(f"{name} свободен только с {free_at}")
            continue
        return None
    if problems:
        return "; ".join(problems)
    return "нет свободного курьера"


def assess_store(store, order):
    """Время обслуживания и короткая причина, если магазин заказ не берёт."""
    store_coords = store.coords
    order_coords = order.user_coords
    store_stock = store.stock.copy()
    missing = []
    found = 0
    for item in order.items:
        if item in store_stock:
            store_stock.remove(item)
            found += 1
        else:
            missing.append(item.title)
    time_to_assemble = assemble_seconds(found)
    if time_to_assemble == 0:
        if missing:
            return math.inf, f"нет товаров: {_names(missing)}"
        return math.inf, "в заказе нет товаров"
    total_time = deliver_seconds(store_coords, order_coords) + time_to_assemble
    remark = f"нет в наличии: {_names(missing)}" if missing else ""
    if len(store.list_of_storekeepers) == 0:
        reason = "нет кладовщика"
        if remark:
            reason = f"{remark}; {reason}"
        return math.inf, reason
    if len(store.list_of_couriers) == 0:
        reason = "нет курьера"
        if remark:
            reason = f"{remark}; {reason}"
        return math.inf, reason
    keeper_problem = _keeper_problem(store, order, time_to_assemble)
    if keeper_problem:
        if remark:
            keeper_problem = f"{remark}; {keeper_problem}"
        return math.inf, keeper_problem
    courier_problem = _courier_problem(store, order, time_to_assemble, total_time)
    if courier_problem:
        if remark:
            courier_problem = f"{remark}; {courier_problem}"
        return math.inf, courier_problem
    return total_time, remark


def calculate_order_time(store, order):
    # Функция для расчета времени обработки заказа
    total_time, _remark = assess_store(store, order)
    return total_time


def get_fastest_store(stores: list, order):
    # Функция для определения самого быстрого магазина для обработки заказа
    min_time = math.inf
    fastest_store = None
    assessed = []
    for store in stores:
        total_time, remark = assess_store(store, order)
        assessed.append((store, total_time, remark))
        if total_time <= min_time:
            min_time = total_time
            fastest_store = store
    if min_time == math.inf:
        fastest_store = None
        order.comment = "; ".join(
            f"магазин {store.id_of_store}: {remark}" for store, _total, remark in assessed
        )
    console_view.print_store_choice(order, assessed, fastest_store, min_time)
    return fastest_store


def is_courier_a_schoolboy():
    number = random.randint(1, 10)
    if number == 1:
        return True
    return False


def send_order_to_fastest_store(stores, order):
    fastest_store = get_fastest_store(stores, order)
    if fastest_store is None:
        order.status = 'не принят'
        return
    fastest_store.take_order(order)
