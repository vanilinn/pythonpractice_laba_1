"""Чистые правила планирования заказа.

Модуль не печатает, не читает ввод и не изменяет переданные объекты.
"""

from dataclasses import dataclass
from datetime import timedelta
import math

from calculations import order_service_time, pick_items, worker_unavailable


@dataclass(frozen=True, slots=True)
class OrderPlan:
    remaining_stock: tuple
    picked_items: tuple
    missing_items: tuple
    total_time: float
    assemble_time: int
    deliver_time: int | None
    storekeeper: object | None
    courier: object | None
    remark: str

    @property
    def can_be_served(self):
        return self.total_time != math.inf


@dataclass(frozen=True, slots=True)
class StoreAssessment:
    store: object
    total_time: float
    remark: str


@dataclass(frozen=True, slots=True)
class StoreSelection:
    assessments: tuple[StoreAssessment, ...]
    fastest_store: object | None
    min_time: float


def _names(items):
    return ", ".join(item.title for item in items)


def _with_remark(remark, reason):
    return f"{remark}; {reason}" if remark else reason


def _available_worker(
    workers,
    order_start,
    must_be_free_by,
    needed_seconds,
    task,
):
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
            return worker, ""
        problems.append(reason)
    return None, "; ".join(problems)


def build_order_plan(store, order):
    """Построить неизменяемый план без выполнения заказа."""
    remaining, picked, missing = pick_items(store.stock, order.items)
    total, assemble, _missing_titles = order_service_time(
        store.stock,
        order.items,
        store.coords,
        order.user_coords,
    )
    if total == math.inf:
        reason = f"нет товаров: {_names(missing)}" if missing else "в заказе нет товаров"
        return OrderPlan(
            tuple(remaining), tuple(picked), tuple(missing), math.inf,
            assemble, None, None, None, reason,
        )

    remark = f"нет в наличии: {_names(missing)}" if missing else ""
    deliver = total - assemble
    if not store.list_of_storekeepers:
        return OrderPlan(
            tuple(remaining), tuple(picked), tuple(missing), math.inf,
            assemble, deliver, None, None, _with_remark(remark, "нет кладовщика"),
        )
    if not store.list_of_couriers:
        return OrderPlan(
            tuple(remaining), tuple(picked), tuple(missing), math.inf,
            assemble, deliver, None, None, _with_remark(remark, "нет курьера"),
        )

    keeper, keeper_problem = _available_worker(
        store.list_of_storekeepers,
        order.time_start,
        order.time_start,
        assemble,
        "собрать",
    )
    if keeper is None:
        return OrderPlan(
            tuple(remaining), tuple(picked), tuple(missing), math.inf,
            assemble, deliver, None, None, _with_remark(remark, keeper_problem),
        )

    courier_ready_at = order.time_start + timedelta(seconds=assemble)
    courier, courier_problem = _available_worker(
        store.list_of_couriers,
        order.time_start,
        courier_ready_at,
        total,
        "доставить",
    )
    if courier is None:
        return OrderPlan(
            tuple(remaining), tuple(picked), tuple(missing), math.inf,
            assemble, deliver, keeper, None, _with_remark(remark, courier_problem),
        )

    return OrderPlan(
        tuple(remaining), tuple(picked), tuple(missing), total,
        assemble, deliver, keeper, courier, remark,
    )


def select_fastest_store(stores, order):
    """Выбрать магазин; при равенстве сохранить прежний выбор последнего."""
    assessments = tuple(
        StoreAssessment(store, *assess_store(store, order))
        for store in stores
    )
    min_time = math.inf
    fastest = None
    for assessment in assessments:
        if assessment.total_time <= min_time:
            min_time = assessment.total_time
            fastest = assessment.store
    if min_time == math.inf:
        fastest = None
    return StoreSelection(assessments, fastest, min_time)


def assess_store(store, order):
    plan = build_order_plan(store, order)
    return plan.total_time, plan.remark
