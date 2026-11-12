import random

import console_view
from order_planning import assess_store as assess_store_data
from order_planning import select_fastest_store


def assess_store(store, order):
    """Время обслуживания и короткая причина, если магазин заказ не берёт."""
    return assess_store_data(store, order)


def calculate_order_time(store, order):
    # Функция для расчета времени обработки заказа
    total_time, _remark = assess_store(store, order)
    return total_time


def get_fastest_store(stores: list, order):
    """Действие: применить и показать результат чистого выбора магазина."""
    selection = select_fastest_store(stores, order)
    assessed = [
        (assessment.store, assessment.total_time, assessment.remark)
        for assessment in selection.assessments
    ]
    if selection.fastest_store is None:
        order.comment = "; ".join(
            f"магазин {store.id_of_store}: {remark}" for store, _total, remark in assessed
        )
    console_view.print_store_choice(
        order,
        assessed,
        selection.fastest_store,
        selection.min_time,
    )
    return selection.fastest_store


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
