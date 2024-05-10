from dataclasses import dataclass


@dataclass
class Item:
    title: str
    cost: int
    provider_id: int | None
    store_id: int | None

    def __str__(self):
        return f'Товар {self.title} стоимостью {self.cost} из магазина {self.store_id} от поставщика {self.provider_id} \n'
