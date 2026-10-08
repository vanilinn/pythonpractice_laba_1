"""Расчёты заказа. Одинаковые аргументы дают одинаковый результат и ничего не меняют снаружи."""

import math


def assemble_seconds(item_count):
    """45 секунд на каждый товар, который есть в наличии."""
    return item_count * 45


def deliver_seconds(store_coords, user_coords):
    """Дорога до покупателя, минута на передачу и минута запаса."""
    distance = round(math.sqrt(
        (store_coords[0] - user_coords[0]) ** 2
        + (store_coords[1] - user_coords[1]) ** 2
    ))
    return distance * 30 + 120


def service_pay(seconds):
    """5 рублей за каждую полную минуту сборки или доставки."""
    if not seconds or seconds == float("inf"):
        return 0
    return int(seconds) * 5 // 60
