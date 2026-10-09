from datetime import timedelta, datetime

from courier import Courier
from item import Item
from order import Order
from provider import Provider
from storekeeper import Storekeeper
from calculations import append_item, append_items, assemble_seconds, deliver_seconds, pick_items, worker_unavailable
import console_view


class Store:
    def __init__(self, id_of_store: int | str, coords: tuple[int, int], stock: list[Item],
                 list_of_providers: list[Provider], schedule: list[datetime, datetime]):
        self.id_of_store = id_of_store
        self.coords: tuple[int, int] = coords
        self.stock = stock
        self.list_of_providers: list[Provider] = list_of_providers
        self.list_of_storekeepers: list[Storekeeper] = []
        self.list_of_couriers: list[Courier] = []
        self.list_of_orders_in_process: list[Order] = []
        self.schedule = schedule

    def send_request(self, request: list[Item], reason="поставка"):
        arrived = []
        for provider in self.list_of_providers:
            response = provider.send_order(request)
            for elem in response:
                elem.store_id = self.id_of_store
            provider.update_stocks()
            self.stock = append_items(self.stock, response)
            arrived.extend(response)
        console_view.print_supply(self.id_of_store, arrived, reason)

    # send_request - отправить заказ для провайдера (что привезти)

    def take_order(self, order: Order):  # принять заказ и начать его обрабатывать
        self.stock, picked, missing_items = pick_items(self.stock, order.items)
        order.existing_items = picked
        missing = [item.title for item in missing_items]
        # order.existing_items = [item for item in order.items if item in self.stock]
        if len(order.existing_items) == 0:
            console_view.print_nothing_in_stock(order)
            return None
        if missing:
            command = console_view.ask_partial_order(self.id_of_store, missing)
            if command == 'no':
                returned = list(order.existing_items)
                self.stock = append_items(self.stock, returned)
                order.existing_items = []
                order.status = 'отменен'
                order.comment = f"на склад возвращено: {', '.join(item.title for item in returned)}"
                console_view.print_order_cancelled(order, returned)
                return None
            console_view.print_order_continued()
        self.send_request(order.existing_items, reason="пополнение")
        # self.send_request(order.existing_items)
        order.time_to_assemble = assemble_seconds(len(order.existing_items))
        order.time_to_deliver = deliver_seconds(self.coords, order.user_coords)
        console_view.print_timing(order)
        if len(self.list_of_couriers) == 0:
            console_view.print_no_couriers()
            return None
        elif len(self.list_of_storekeepers) == 0:
            console_view.print_no_storekeepers()
            return None
        for storekeeper in self.list_of_storekeepers:
            if worker_unavailable(
                storekeeper.get_name(),
                storekeeper.get_status(),
                storekeeper.get_job_start(),
                storekeeper.get_job_end(),
                order.time_start,
                order.time_start,
                order.time_to_assemble,
                "собрать",
            ) is None:
                order.status = 'собирается'
                order.assembler = storekeeper.get_worker_id()
                storekeeper.order_id = order.id
                storekeeper.get_order(self, order)
                break
        if not order.assembler:
            console_view.print_assemble_too_late()
            return None
        for courier in self.list_of_couriers:
            courier_ready_at = order.time_start + timedelta(seconds=order.time_to_assemble)
            if worker_unavailable(
                courier.get_name(),
                courier.get_status(),
                courier.get_job_start(),
                courier.get_job_end(),
                order.time_start,
                courier_ready_at,
                order.time_to_assemble + order.time_to_deliver,
                "доставить",
            ) is None:
                order.status = 'доставляется'
                order.courier = courier.get_worker_id()
                courier.order_id = order.id
                courier.get_order(self, order)
                break

        if not order.courier:
            console_view.print_delivery_too_late()
            return None

    def get_worker(self, worker):
        if isinstance(worker, Courier):
            self.list_of_couriers = append_item(self.list_of_couriers, worker)

        elif isinstance(worker, Storekeeper):
            self.list_of_storekeepers = append_item(self.list_of_storekeepers, worker)
        worker.set_store_id(self.id_of_store)

    # взять работника к себе и дать ему смену

    def __str__(self):
        lines = [
            f"Магазин {self.id_of_store}, координаты {console_view.format_coords(self.coords)}",
            "График: " + console_view.format_hours(self.schedule[0], self.schedule[1]),
            "Склад:",
        ]
        if not self.stock:
            lines.append("  пусто")
        else:
            for el in self.stock:
                lines.append("  " + console_view.item_line(el))
        return "\n".join(lines)
