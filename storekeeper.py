from calculations import service_pay
from order import Order
# from store import Store
from worker import Worker
import console_view
from datetime import datetime, timedelta


class Storekeeper(Worker):
    def __init__(self, worker_id, name):
        super().__init__(worker_id=worker_id, name=name)
        self.__worker_id = worker_id
        self.__store_id = None
        self.__name = name
        self.__status = 'безработный'
        self.__order_id = None
        self.__job_start = None
        self.__job_end = None
        self.__balance = 0

    def get_shift(self, store, job_time: int):
        # Метод для начала смены кладовщика
        self.__job_start = datetime(2022, 1, 1, 9, 0, 0)  # Устанавливаем начало смены на 9:00 утра
        if store.schedule[0] > self.__job_start:
            self.__job_start = store.schedule[0]  # Если магазин открывается позже, корректируем время начала работы кладовщика
        if store.schedule[1] < self.__job_start + timedelta(hours=job_time):
            self.__job_end = store.schedule[1]  # Если смена продлится дольше, чем закрывается магазин, корректируем время окончания работы кладовщика
        else:
            self.__job_end = self.__job_start + timedelta(
                hours=job_time)  # В противном случае, устанавливаем время окончания смены
        self.__store_id = store.id_of_store  # Записываем идентификатор магазина
        self.__status = 'свободен'  # Устанавливаем статус "свободен" для кладовщика
        store.get_worker(self)  # Добавляем кладовщика в список работников магазина
        console_view.print_shift_started(
            "кладовщик", self.__name, store.id_of_store, job_time, self.__job_start, self.__job_end
        )

    def get_order(self, store, order: Order):
        # Метод для получения заказа кладовщиком
        job_time = order.time_to_assemble  # Время, необходимое на сборку заказа
        self.__status = 'собирает'  # Устанавливаем статус "собирает" для кладовщика
        self.__job_start = order.time_start + timedelta(seconds=job_time)  # Устанавливаем время окончания сборки заказа
        earned = service_pay(job_time)
        self.set_balance(
            self.get_balance() + earned)  # Добавляем к балансу кладовщика оплату за сборку заказа
        order.status = 'собран'  # Устанавливаем статус заказа как "собран"
        self.__status = 'свободен'  # Устанавливаем статус "свободен" для кладовщика
        console_view.print_order_packed(self.__name, order, earned, self.get_balance())
        self.__order_id = None  # Обнуляем идентификатор заказа

    def get_job_start(self):
        return self.__job_start

    def get_job_end(self):
        return self.__job_end

    def get_worker_id(self):
        return self.__worker_id

    def is_still_working(self):
        time_left = (self.__job_end - datetime.now()).total_seconds()
        if time_left > 0:
            return True
        else:
            return False

    def get_order_id(self):
        return self.__order_id

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def get_balance(self):
        return self.__balance

    def set_store_id(self, store_id):
        self.__store_id = store_id

    def get_name(self):
        return self.__name

    def get_status(self):
        return self.__status

    def get_store_id(self):
        return self.__store_id

    def set_status(self, status):
        self.__status = status

    def set_balance(self, balance):
        self.__balance = balance

    def __str__(self):
        return (
            f"Кладовщик {self.__name}, {self.__status}, магазин {self.__store_id}, "
            f"{console_view.format_money(self.__balance)}"
        )
