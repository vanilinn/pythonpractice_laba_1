"""Проверки вычислений отдельно от магазинов, печати и ввода."""

import math
import unittest
from datetime import datetime, timedelta

from calculations import (
    append_item,
    assemble_seconds,
    deliver_seconds,
    order_service_time,
    pick_items,
    service_pay,
    worker_unavailable,
    without_first,
)
from item import Item
from order import make_order


def item(title, cost=10):
    return Item(title, cost, 1, None)


class AssembleAndDeliveryTests(unittest.TestCase):
    def test_empty_order_takes_no_time_to_assemble(self):
        self.assertEqual(assemble_seconds(0), 0)

    def test_one_item_takes_45_seconds(self):
        self.assertEqual(assemble_seconds(1), 45)

    def test_several_items_take_45_seconds_each(self):
        self.assertEqual(assemble_seconds(3), 135)

    def test_delivery_without_distance_is_two_minutes(self):
        self.assertEqual(deliver_seconds((1, 1), (1, 1)), 120)

    def test_same_coordinates_give_the_same_delivery_time(self):
        first = deliver_seconds((1, 1), (10, 10))
        second = deliver_seconds((1, 1), (10, 10))
        self.assertEqual(first, second)
        self.assertEqual(first, 510)


class ServicePayTests(unittest.TestCase):
    def test_no_work_pays_nothing(self):
        self.assertEqual(service_pay(0), 0)
        self.assertEqual(service_pay(None), 0)

    def test_pay_grows_only_on_a_full_minute(self):
        self.assertEqual(service_pay(59), 4)
        self.assertEqual(service_pay(60), 5)

    def test_same_seconds_give_the_same_pay(self):
        self.assertEqual(service_pay(90), service_pay(90))
        self.assertEqual(service_pay(90), 7)


class PickItemsTests(unittest.TestCase):
    def test_empty_stock_picks_nothing(self):
        cookie = item("печенье")
        remaining, picked, missing = pick_items([], [cookie])
        self.assertEqual(remaining, [])
        self.assertEqual(picked, [])
        self.assertEqual(missing, [cookie])

    def test_one_available_item_is_picked(self):
        cookie = item("печенье")
        bread = item("хлеб")
        remaining, picked, missing = pick_items([cookie], [cookie, bread])
        self.assertEqual(remaining, [])
        self.assertEqual(picked, [cookie])
        self.assertEqual(missing, [bread])

    def test_several_items_keep_the_ones_not_ordered(self):
        cookie = item("печенье", 100)
        bread = item("хлеб", 20)
        milk = item("молоко", 30)
        remaining, picked, missing = pick_items(
            [cookie, bread, milk],
            [cookie, bread],
        )
        self.assertEqual(picked, [cookie, bread])
        self.assertEqual(remaining, [milk])
        self.assertEqual(missing, [])

    def test_input_lists_stay_unchanged(self):
        cookie = item("печенье")
        bread = item("хлеб")
        stock = [cookie, bread]
        order = [cookie]
        stock_before = list(stock)
        order_before = list(order)
        pick_items(stock, order)
        without_first(stock, cookie)
        append_item(stock, bread)
        self.assertEqual(stock, stock_before)
        self.assertEqual(order, order_before)

    def test_same_arguments_give_the_same_split(self):
        cookie = item("печенье")
        stock = [cookie]
        order = [cookie]
        self.assertEqual(pick_items(stock, order), pick_items(stock, order))


class OrderServiceTimeTests(unittest.TestCase):
    def test_empty_match_cannot_be_served(self):
        total, assemble, missing = order_service_time([], [item("пиво")], (1, 1), (10, 10))
        self.assertEqual(total, math.inf)
        self.assertEqual(assemble, 0)
        self.assertEqual(missing, ["пиво"])

    def test_known_route_adds_assembly_and_delivery(self):
        goods = [item("печенье"), item("хлеб"), item("пиво")]
        total, assemble, missing = order_service_time(goods, goods, (1, 1), (10, 10))
        self.assertEqual(assemble, 135)
        self.assertEqual(total, 135 + 510)
        self.assertEqual(missing, [])


class WorkerAvailabilityTests(unittest.TestCase):
    def setUp(self):
        self.start = datetime(2022, 1, 1, 10, 0, 0)
        self.end = datetime(2022, 1, 1, 19, 0, 0)

    def test_free_worker_with_enough_time_is_available(self):
        reason = worker_unavailable(
            "Кладовщик1", "свободен", self.start, self.end, self.start, self.start, 45, "собрать"
        )
        self.assertIsNone(reason)

    def test_exact_end_of_shift_is_still_enough(self):
        needed = (self.end - self.start).total_seconds()
        reason = worker_unavailable(
            "Кладовщик1", "свободен", self.start, self.end, self.start, self.start, needed, "собрать"
        )
        self.assertIsNone(reason)

    def test_one_second_past_shift_is_not_enough(self):
        needed = (self.end - self.start).total_seconds() + 1
        reason = worker_unavailable(
            "Кладовщик1", "свободен", self.start, self.end, self.start, self.start, needed, "собрать"
        )
        self.assertEqual(reason, "Кладовщик1 не успевает собрать до конца смены")

    def test_busy_worker_is_named_with_status(self):
        reason = worker_unavailable(
            "Курьер1", "доставляет", self.start, self.end, self.start, self.start, 45, "доставить"
        )
        self.assertEqual(reason, "Курьер1 занят (доставляет)")

    def test_worker_free_later_reports_the_clock_time(self):
        free_at = self.start + timedelta(minutes=3)
        reason = worker_unavailable(
            "Кладовщик1", "свободен", free_at, self.end, self.start, self.start, 45, "собрать"
        )
        self.assertEqual(reason, "Кладовщик1 свободен только с 10:03")


class MakeOrderTests(unittest.TestCase):
    def test_same_arguments_build_the_same_order(self):
        goods = [item("хлеб", 20)]
        moment = datetime(2022, 1, 1, 10, 0, 0)
        first = make_order("order-1", goods, moment, "user-1", (10, 10))
        second = make_order("order-1", goods, moment, "user-1", (10, 10))
        self.assertEqual(first, second)
        self.assertEqual(first.status, "создан")

    def test_order_keeps_its_own_item_list(self):
        bread = item("хлеб", 20)
        goods = [bread]
        order = make_order("order-1", goods, datetime(2022, 1, 1, 10, 0, 0), "user-1", (10, 10))
        goods.append(item("молоко", 30))
        self.assertEqual(order.items, [bread])
        self.assertEqual(len(goods), 2)


if __name__ == "__main__":
    unittest.main()
