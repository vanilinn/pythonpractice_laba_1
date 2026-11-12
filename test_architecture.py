"""Характеризационные тесты границ и выделенных слоёв."""

import contextlib
from datetime import datetime
import importlib
import io
import math
import sys
import unittest

from courier import Courier
from item import Item
from order import make_order
from order_planning import build_order_plan, select_fastest_store
from provider import Provider
from reporting import build_receipt
from store import Store
from storekeeper import Storekeeper


NOW = datetime(2022, 1, 1, 10)
SCHEDULE = [datetime(2022, 1, 1, 9), datetime(2022, 1, 1, 21)]


def product(title="хлеб", cost=20):
    return Item(title, cost, 1, None)


def order_for(items):
    return make_order("order-1", items, NOW, "user-1", (1, 1))


class ProviderCharacterizationTests(unittest.TestCase):
    def test_update_restores_original_assortment_once(self):
        bread = product()
        provider = Provider(1, [bread])
        self.assertEqual(provider.send_order([bread]), [bread])
        provider.update_stocks()
        self.assertEqual(provider.send_order([bread]), [bread])

    def test_store_assignment_uses_copy_on_write(self):
        bread = product()
        provider = Provider(1, [bread])
        store = Store(7, (1, 1), [], [provider], SCHEDULE)
        with contextlib.redirect_stdout(io.StringIO()):
            store.send_request([bread])
        self.assertIsNone(bread.store_id)
        self.assertEqual(store.stock[0].store_id, 7)
        self.assertIsNot(store.stock[0], bread)


class PlanningTests(unittest.TestCase):
    def test_plan_is_deterministic_and_does_not_change_stock(self):
        bread = product()
        store = Store(1, (1, 1), [bread], [], SCHEDULE)
        order = order_for([bread])
        before = list(store.stock)
        first = build_order_plan(store, order)
        second = build_order_plan(store, order)
        self.assertEqual(first, second)
        self.assertEqual(store.stock, before)
        self.assertEqual(first.total_time, math.inf)
        self.assertEqual(first.remark, "нет кладовщика")

    def test_equal_times_choose_last_store(self):
        bread = product()
        first = Store(1, (1, 1), [bread], [], SCHEDULE)
        second = Store(2, (1, 1), [bread], [], SCHEDULE)
        with contextlib.redirect_stdout(io.StringIO()):
            for store, suffix in ((first, "1"), (second, "2")):
                Courier(suffix, f"Курьер{suffix}").get_shift(store, 10)
                Storekeeper(suffix, f"Кладовщик{suffix}").get_shift(store, 10)
        selection = select_fastest_store([first, second], order_for([bread]))
        self.assertIs(selection.fastest_store, second)


class BoundaryTests(unittest.TestCase):
    def test_partial_order_decision_is_injected(self):
        bread = product()
        milk = product("молоко", 30)
        store = Store(1, (1, 1), [bread], [], SCHEDULE)
        order = order_for([bread, milk])
        decisions = []

        def reject(store_id, missing):
            decisions.append((store_id, missing))
            return "no"

        with contextlib.redirect_stdout(io.StringIO()):
            store.take_order(order, decide_partial=reject)
        self.assertEqual(decisions, [(1, ["молоко"])])
        self.assertEqual(order.status, "отменен")
        self.assertEqual(store.stock, [bread])

    def test_receipt_builder_is_pure(self):
        bread = product()
        order = order_for([bread])
        order.existing_items = [bread]
        order.time_to_assemble = 45
        order.time_to_deliver = 120
        receipt = build_receipt(order)
        self.assertEqual(receipt.total, 33)
        self.assertEqual(receipt.rows[-1], ("доставка", 10))

    def test_importing_main_has_no_output(self):
        sys.modules.pop("main", None)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            importlib.import_module("main")
        self.assertEqual(output.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
