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


def append_item(items, item):
    """Новый список с элементом в конце. Исходный список не меняется."""
    result = list(items)
    result.append(item)
    return result


def append_items(items, extra):
    """Новый список, в конец которого добавлены все элементы extra."""
    result = list(items)
    result.extend(extra)
    return result


def without_first(items, item):
    """Новый список без первого вхождения item. Исходный список не меняется."""
    result = list(items)
    if item in result:
        result.remove(item)
    return result


def pick_items(stock, items):
    """Новый остаток, что удалось взять и чего не было. Входные списки не меняются."""
    remaining = list(stock)
    picked = []
    missing = []
    for item in items:
        if item in remaining:
            remaining = without_first(remaining, item)
            picked = append_item(picked, item)
        else:
            missing = append_item(missing, item)
    return remaining, picked, missing


def count_available(stock, items):
    """Сколько позиций заказа есть в переданном списке и каких не хватает."""
    _remaining, picked, missing = pick_items(stock, items)
    return len(picked), [item.title for item in missing]


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
