import time
import uuid
from datetime import datetime

from item import Item
from order import Order


class User:
    def __init__(self, name, coords: tuple[int, int]):
        self.id = uuid.uuid4().hex
        self.name = name
        self.coords: tuple[int, int] = coords

    def make_order(self, items: list[Item]):
        return Order(
            id=uuid.uuid4().hex,
            items=items,
            status='создан',
            existing_items=[],
            time_to_assemble=None,
            time_to_deliver=None,
            time_start=datetime.now(),
            time_end=None,
            assembler=None,
            courier=None,
            user_id=self.id,
            user_coords=self.coords
        )

    # сделать заказ

    def take_order(self):
        print('Заказ принят')

    # забрать заказ

    def __str__(self):
        return f'Пользователь {self.name} с координатами {self.coords}'
