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


def count_available(stock, items):
    """Сколько позиций заказа есть в переданном списке и каких не хватает."""
    remaining = list(stock)
    missing = []
    found = 0
    for item in items:
        if item in remaining:
            remaining.remove(item)
            found += 1
        else:
            missing.append(item.title)
    return found, missing


def order_service_time(stock, items, store_coords, user_coords):
    """Полное время заказа по складу, составу и двум точкам."""
    found, missing = count_available(stock, items)
    assemble = assemble_seconds(found)
    if assemble == 0:
        return math.inf, assemble, missing
    total = deliver_seconds(store_coords, user_coords) + assemble
    return total, assemble, missing


def worker_unavailable(name, status, job_start, job_end, order_start, must_be_free_by, needed_seconds, task):
    """None, если человек успевает. Иначе короткая причина отказа."""
    if status != "свободен":
        return f"{name} занят ({status})"
    if job_start > must_be_free_by:
        return f"{name} свободен только с {job_start.strftime('%H:%M')}"
    time_left = (job_end - order_start).total_seconds()
    if time_left < needed_seconds:
        return f"{name} не успевает {task} до конца смены"
    return None
