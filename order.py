from dataclasses import dataclass
from datetime import datetime
from item import Item


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

    def __str__(self):
        return f'Заказ {self.id} состоящий из {[f"Товар {el.title} стоимостью {el.cost} из магазина {el.store_id} от поставщика {el.provider_id} " for el in self.items]}, Статус: {self.status}, Время создания заказа: {self.time_start}, Время доставки: {self.time_end}, Собирает: {self.assembler}, Доставляет: {self.courier}, Пользователь: {self.user_id}'

# Что находится в заказе? Статус доставки, список товаров, время создания-время доставки, кто собирал-доставлял
