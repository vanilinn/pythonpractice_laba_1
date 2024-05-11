from dataclasses import dataclass
from datetime import datetime
from item import Item
import console_view


@dataclass
class Order:
    id: int | str
    items: list[Item]
    existing_items: list[Item]
    status: str
    time_to_assemble: int | None
    time_to_deliver: int | None
    time_start: datetime
    time_end: datetime | None
    assembler: int | str | None
    courier: int | str | None
    user_id: int | str
    user_coords: tuple[int, int] | None
    comment: str | None = None

    def __str__(self):
        goods = ", ".join(console_view.item_line(el) for el in self.items) or "пусто"
        comment = f"\n  {self.comment}" if self.comment else ""
        return (
            f"Заказ {console_view.short_id(self.id)}, {self.status}, "
            f"{console_view.format_clock(self.time_start)}\n"
            f"  {goods}{comment}"
        )

# Что находится в заказе? Статус доставки, список товаров, время создания-время доставки, кто собирал-доставлял
