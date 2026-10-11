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


def make_order(order_id, items, time_start, user_id, user_coords):
    """Форма заказа. Идентификатор и время приходят снаружи, а не из часов и генератора."""
    return Order(
        id=order_id,
        items=list(items),
        status="создан",
        existing_items=[],
        time_to_assemble=None,
        time_to_deliver=None,
        time_start=time_start,
        time_end=None,
        assembler=None,
        courier=None,
        user_id=user_id,
        user_coords=user_coords,
    )

# Что находится в заказе? Статус доставки, список товаров, время создания-время доставки, кто собирал-доставлял
