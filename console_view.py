"""Короткий текстовый вывод хода сценария."""

from datetime import datetime


def short_id(value):
    if value is None:
        return "—"
    text = str(value)
    if len(text) <= 12:
        return text
    return text[:8]


def format_clock(moment):
    if moment is None:
        return "—"
    if isinstance(moment, datetime):
        return moment.strftime("%H:%M")
    return str(moment)


def format_hours(start, end):
    return f"{format_clock(start)}-{format_clock(end)}"


def format_duration(seconds):
    if seconds is None:
        return "—"
    if seconds == float("inf"):
        return "невозможно"
    total = int(seconds)
    hours, remainder = divmod(abs(total), 3600)
    minutes, secs = divmod(remainder, 60)
    parts = []
    if hours:
        parts.append(f"{hours} ч")
    if minutes:
        parts.append(f"{minutes} мин")
    if secs or not parts:
        parts.append(f"{secs} сек")
    text = " ".join(parts)
    if total < 0:
        return f"-{text}"
    return text


def format_money(amount):
    return f"{amount} руб."


def format_coords(coords):
    if coords is None:
        return "—"
    return f"({coords[0]}, {coords[1]})"


def service_fee(seconds):
    """Та же ставка, что у оплаты кладовщика и курьера: 5 руб. за полную минуту."""
    if not seconds or seconds == float("inf"):
        return 0
    return int(seconds) * 5 // 60


def item_line(item):
    return f"{item.title}, {format_money(item.cost)}"


def heading(text):
    print()
    print(text)


def line(text, indent=1):
    print(f"{'  ' * indent}{text}")


def print_intro():
    print("Доставка из магазинов. Время в журнале — 1 января 2022 года.")


def print_user(user):
    line(f"{user.name} {format_coords(user.coords)}")


def print_order_created(user, order):
    goods = ", ".join(item.title for item in order.items) or "пусто"
    line(f"{short_id(order.id)}  {user.name}  {format_clock(order.time_start)}  {goods}")


def print_supply(store_id, items, reason):
    if not items:
        return
    goods = ", ".join(item_line(item) for item in items)
    line(f"Магазин {store_id}, {reason}: {goods}")


def print_shift_started(role, name, store_id, requested_hours, job_start, job_end):
    line(f"{role.capitalize()} {name}, магазин {store_id}, смена {format_hours(job_start, job_end)}")


def print_store_choice(order, assessed, fastest, seconds):
    heading(f"Заказ {short_id(order.id)}")
    for store, total, remark in assessed:
        if total == float("inf"):
            line(f"Магазин {store.id_of_store}: отказ, {remark}")
        elif remark:
            line(f"Магазин {store.id_of_store}: {format_duration(total)}, {remark}")
        else:
            line(f"Магазин {store.id_of_store}: {format_duration(total)}")
    if fastest is None or seconds == float("inf"):
        line("Заказ не принят.")
        return
    line(f"Выбран магазин {fastest.id_of_store}.")


def print_nothing_in_stock(order):
    line(f"В выбранном магазине нет товаров заказа {short_id(order.id)}.")


def ask_partial_order(store_id, missing_titles):
    missing = ", ".join(missing_titles)
    line(f"В магазине {store_id} нет: {missing}.")
    command = ""
    while command != "yes" and command != "no":
        command = input("  Собрать без них? yes/no: ")
    return command


def print_order_cancelled(order, returned_items):
    names = ", ".join(item.title for item in returned_items) or "нечего возвращать"
    line(f"Заказ {short_id(order.id)} отменён. На склад возвращено: {names}.")


def print_order_continued():
    line("Собираем только то, что есть на складе.")


def print_no_couriers():
    line("Остановка: в магазине нет курьера.")


def print_no_storekeepers():
    line("Остановка: в магазине нет кладовщика.")


def print_timing(order):
    line(
        f"Сборка {format_duration(order.time_to_assemble)}, "
        f"доставка {format_duration(order.time_to_deliver)}."
    )


def print_assemble_too_late():
    line("Остановка: кладовщик не успевает собрать заказ до конца смены.")


def print_delivery_too_late():
    line("Остановка: курьер не успевает доставить заказ до конца смены.")


def print_order_packed(keeper_name, order, earned, balance):
    names = ", ".join(item.title for item in order.existing_items)
    line(f"{keeper_name} собрал: {names}. Начислено {format_money(earned)}, баланс {format_money(balance)}")


def print_delivery_started(courier_name, order):
    line(f"{courier_name} везёт заказ, в пути {format_duration(order.time_to_deliver)}.")


def print_order_status(order, courier_name):
    line(f"Заказ {short_id(order.id)} доставлен, курьер {courier_name}.")


def print_courier_left_without_pay(courier_name, store_id):
    line(f"{courier_name} не вернулся в магазин {store_id}. Оплата курьеру не начислена.")


def print_courier_back(courier_name, store_id, returned_at):
    line(f"{courier_name} снова свободен в магазине {store_id} с {format_clock(returned_at)}.")


def print_courier_pay(courier_name, earned, balance):
    line(f"{courier_name}: за доставку {format_money(earned)}, баланс {format_money(balance)}")


def print_receipt(order):
    rows = [(item.title, item.cost) for item in order.existing_items]
    goods = sum(amount for _, amount in rows)
    assembly = service_fee(order.time_to_assemble)
    delivery = service_fee(order.time_to_deliver)
    rows.append(("сборка", assembly))
    rows.append(("доставка", delivery))
    total = goods + assembly + delivery
    label_width = max(len(name) for name, _ in rows)
    line("Чек")
    for name, amount in rows:
        line(f"{name:<{label_width}}  {amount:>4} руб.", indent=2)
    line(f"{'итого':<{label_width}}  {total:>4} руб.", indent=2)
    return total


def print_user_accepted():
    line("Покупатель забрал заказ.")


def user_name(user_id, users):
    for user in users:
        if user.id == user_id:
            return user.name
    return short_id(user_id)


def worker_name(worker_id, workers):
    if worker_id is None:
        return "—"
    for worker in workers:
        if worker.get_worker_id() == worker_id:
            return worker.get_name()
    return str(worker_id)


def print_session_report(stores, orders, users, couriers, storekeepers):
    heading("Итог")
    for order in orders:
        buyer = user_name(order.user_id, users)
        extra = ""
        if order.status == "доставлен" and order.existing_items:
            goods = sum(item.cost for item in order.existing_items)
            total = goods + service_fee(order.time_to_assemble) + service_fee(order.time_to_deliver)
            extra = f", к оплате {format_money(total)}"
        elif getattr(order, "comment", None):
            extra = f", {order.comment}"
        line(f"{short_id(order.id)}  {order.status}  {buyer}{extra}")

    heading("Склады")
    for store in stores:
        if store.stock:
            goods = ", ".join(item_line(item) for item in store.stock)
        else:
            goods = "пусто"
        line(f"Магазин {store.id_of_store}: {goods}")

    heading("Сотрудники")
    for keeper in storekeepers:
        line(
            f"{keeper.get_name()}, магазин {keeper.get_store_id()}, "
            f"{keeper.get_status()}, {format_money(keeper.get_balance())}"
        )
    for courier in couriers:
        line(
            f"{courier.get_name()}, магазин {courier.get_store_id()}, "
            f"{courier.get_status()}, {format_money(courier.get_balance())}"
        )

    delivered = sum(1 for order in orders if order.status == "доставлен")
    cancelled = sum(1 for order in orders if order.status == "отменен")
    declined = sum(1 for order in orders if order.status == "не принят")
    keeper_pay = sum(worker.get_balance() for worker in storekeepers)
    courier_pay = sum(worker.get_balance() for worker in couriers)
    heading("Счёт")
    line(f"Заказов {len(orders)}: доставлено {delivered}, отменено {cancelled}, не принято {declined}.")
    line(f"Кладовщикам {format_money(keeper_pay)}, курьерам {format_money(courier_pay)}")
    print()
