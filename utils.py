import math
from datetime import timedelta
import random

from calculations import order_service_time, worker_unavailable
import console_view


def _names(titles):
    return ", ".join(titles)


def _with_remark(remark, reason):
    if remark:
        return f"{remark}; {reason}"
    return reason


def _staff_problem(workers, order_start, must_be_free_by, needed_seconds, task):
    problems = []
    for worker in workers:
        reason = worker_unavailable(
            worker.get_name(),
            worker.get_status(),
            worker.get_job_start(),
            worker.get_job_end(),
            order_start,
            must_be_free_by,
            needed_seconds,
            task,
        )
        if reason is None:
            return None
        problems.append(reason)
    if problems:
        return "; ".join(problems)
    return None


def assess_store(store, order):
    """Время обслуживания и короткая причина, если магазин заказ не берёт."""
    total_time, time_to_assemble, missing = order_service_time(
        store.stock,
        order.items,
        store.coords,
        order.user_coords,
    )
    if total_time == math.inf:
        if missing:
            return math.inf, f"нет товаров: {_names(missing)}"
        return math.inf, "в заказе нет товаров"
    remark = f"нет в наличии: {_names(missing)}" if missing else ""
    if len(store.list_of_storekeepers) == 0:
        return math.inf, _with_remark(remark, "нет кладовщика")
    if len(store.list_of_couriers) == 0:
        return math.inf, _with_remark(remark, "нет курьера")
    keeper_problem = _staff_problem(
        store.list_of_storekeepers,
        order.time_start,
        order.time_start,
        time_to_assemble,
        "собрать",
    )
    if keeper_problem:
        return math.inf, _with_remark(remark, keeper_problem)
    courier_ready_at = order.time_start + timedelta(seconds=time_to_assemble)
    courier_problem = _staff_problem(
        store.list_of_couriers,
        order.time_start,
        courier_ready_at,
        total_time,
        "доставить",
    )
    if courier_problem:
        return math.inf, _with_remark(remark, courier_problem)
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
