import uuid

import console_view


class User:
    def __init__(self, name, coords: tuple[int, int]):
        self.id = uuid.uuid4().hex
        self.name = name
        self.coords: tuple[int, int] = coords

    def take_order(self):
        console_view.print_user_accepted()

    # забрать заказ

    def __str__(self):
        return f"{self.name} {console_view.format_coords(self.coords)}"
