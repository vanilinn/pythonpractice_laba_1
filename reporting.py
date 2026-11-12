"""Чистая подготовка данных для консольных отчётов."""

from dataclasses import dataclass

from calculations import service_pay


@dataclass(frozen=True, slots=True)
class Receipt:
    rows: tuple[tuple[str, int], ...]
    total: int


@dataclass(frozen=True, slots=True)
class SessionSummary:
    delivered: int
    cancelled: int
    declined: int
    keeper_pay: int
    courier_pay: int


def build_receipt(order):
    rows = [(item.title, item.cost) for item in order.existing_items]
    rows.extend((
        ("сборка", service_pay(order.time_to_assemble)),
        ("доставка", service_pay(order.time_to_deliver)),
    ))
    return Receipt(tuple(rows), sum(amount for _, amount in rows))


def build_session_summary(orders, couriers, storekeepers):
    return SessionSummary(
        delivered=sum(order.status == "доставлен" for order in orders),
        cancelled=sum(order.status == "отменен" for order in orders),
        declined=sum(order.status == "не принят" for order in orders),
        keeper_pay=sum(worker.get_balance() for worker in storekeepers),
        courier_pay=sum(worker.get_balance() for worker in couriers),
    )
