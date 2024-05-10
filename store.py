from datetime import timedelta, datetime

from courier import Courier
from item import Item
from order import Order
from provider import Provider
from storekeeper import Storekeeper

import math


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

    def send_request(self, request: list[Item]):
        for provider in self.list_of_providers:
            response = provider.send_order(request)
            for elem in response:
                elem.store_id = self.id_of_store
            provider.update_stocks()
            self.stock.extend(response)

    # send_request - отправить заказ для провайдера (что привезти)

    def take_order(self, order: Order):  # принять заказ и начать его обрабатывать
        print(f'Предметы в заказе: {[item.title for item in order.items]}')
        for item in order.items:
            if item in self.stock:
                self.stock.remove(item)
                order.existing_items.append(item)
            else:
                print(f'Предмета {item.title} нет в наличии в магазине {self.id_of_store}')
        # order.existing_items = [item for item in order.items if item in self.stock]
        self.send_request(order.existing_items)
        if len(order.existing_items) == 0:
            print('Нет предметов в наличии')
            return None
        if len(order.existing_items) < len(order.items):
            command = ''
            while command != 'yes' and command != 'no':
                command = input(
                    f'Некоторых предметов нет в наличии в магазине {self.id_of_store}. Продолжить? yes/no\n')
            if command == 'no':
                print(f'Заказ {order.id} отменен')
                return None
            else:
                print('Отлично, продолжим')
        # self.send_request(order.existing_items)
        order.time_to_assemble = len(order.existing_items) * 45
        order.time_to_deliver = 60 + round(math.sqrt(
            (self.coords[0] - order.user_coords[0]) ** 2 + (self.coords[1] - order.user_coords[1]) ** 2)) * 30 + 60
        if len(self.list_of_couriers) == 0:
            print('Нет свободных курьеров')
            return None
        elif len(self.list_of_storekeepers) == 0:
            print('Нет свободных кладовщиков')
            return None
        for storekeeper in self.list_of_storekeepers:
            time_left = (storekeeper.get_job_end() - order.time_start).total_seconds()
            if storekeeper.get_status() == 'свободен' and time_left >= order.time_to_assemble and storekeeper.get_job_start() <= order.time_start:
                print(f'Кладовщик {storekeeper.get_name()} соберет заказ {order.id}')
                order.status = 'собирается'
                order.assembler = storekeeper.get_worker_id()
                storekeeper.order_id = order.id
                storekeeper.get_order(self, order)
                break
        if not order.assembler:
            print('Заказ не успеют собрать')
            return None
        for courier in self.list_of_couriers:
            time_left = (courier.get_job_end() - order.time_start).total_seconds() - order.time_to_assemble
            if courier.get_status() == 'свободен' and time_left >= order.time_to_deliver and courier.get_job_start() <= order.time_start + timedelta(
                    seconds=order.time_to_assemble):
                print(f'Курьер {courier.get_name()} доставит заказ {order.id}')
                order.status = 'доставляется'
                order.courier = courier.get_worker_id()
                courier.order_id = order.id
                courier.get_order(self, order)
                break

        if not order.courier:
            print('Заказ не успеют доставить')
            return None

    def get_worker(self, worker):
        if isinstance(worker, Courier):
            self.list_of_couriers.append(worker)

        elif isinstance(worker, Storekeeper):
            self.list_of_storekeepers.append(worker)
        worker.set_store_id(self.id_of_store)

    # взять работника к себе и дать ему смену

    def __str__(self):
        return f'{[f"Товар {el.title} стоимостью {el.cost} из магазина {el.store_id} от поставщика {el.provider_id}" for el in self.__stock]}'
