from dataclasses import dataclass

import console_view


@dataclass(frozen=True, slots=True)
class Item:
    title: str
    cost: int
    provider_id: int | None
    store_id: int | None

    def __str__(self):
        return console_view.item_line(self)
