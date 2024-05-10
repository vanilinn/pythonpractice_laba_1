from datetime import datetime, timedelta

from order import Order
from worker import Worker
import utils


class Courier(Worker):
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
        # Метод для начала смены курьера
        self.__job_start = datetime(2022, 1, 1, 9, 0, 0)  # Устанавливаем начало смены на 9:00 утра
        if store.schedule[0] > self.__job_start:
            self.__job_start = store.schedule[
                0]  # Если магазин открывается позже, корректируем время начала работы курьера
        if store.schedule[1] < self.__job_start + timedelta(hours=job_time):
            self.__job_end = store.schedule[
                1]  # Если смена продлится дольше, чем закрывается магазин, корректируем время окончания работы курьера
        else:
            self.__job_end = self.__job_start + timedelta(
                hours=job_time)  # В противном случае, устанавливаем время окончания смены
        self.__store_id = store.id_of_store  # Записываем идентификатор магазина
        self.__status = 'свободен'  # Устанавливаем статус "свободен" для курьера
        store.get_worker(self)  # Добавляем курьера в список работников магазина
        print(f'Курьер {self.__name} вышел на работу в магазин {store.id_of_store} на {job_time} часов')

    def get_order(self, store, order: Order):
        # Метод для получения заказа курьером
        job_time = order.time_to_deliver  # Время, необходимое на доставку заказа
        self.__status = 'доставляет'  # Устанавливаем статус "доставляет" для курьера
        print(f'Курьер {self.__name} доставит заказ {order.id} через {job_time // 60} минут и {job_time % 60} секунд')
        self.__status = 'возвращается'  # Устанавливаем статус "возвращается" для курьера
        print(f'Курьер {self.__name} доставил заказ {order.id} пользователю {order.user_id}')
        order.status = 'доставлен'  # Устанавливаем статус заказа как "доставлен"
        print(f'Заказ {order.id} доставлен курьером {self.__name}')
        if utils.is_courier_a_schoolboy():
            # Проверяем, является ли курьер школьником с помощью функции из модуля utils
            print(f'Курьер {self.__name} не вернулся в магазин {store.id_of_store}, увы, не видать ему денег :(')
            self.__job_start = self.__job_end  # Переопределяем время начала смены курьера
            self.__order_id = None  # Обнуляем идентификатор заказа
            self.__status = 'уволен'  # Устанавливаем статус "уволен" для курьера
            store.list_of_couriers.remove(self)  # Удаляем курьера из списка работников магазина
        else:
            self.__job_start = order.time_start + timedelta(
                seconds=job_time * 2 - 60)  # Вычисляем время возвращения курьера в магазин
            # print(self.__job_start)
            print(f'Курьер {self.__name} вернулся в магазин {store.id_of_store}')
            self.__status = 'свободен'  # Устанавливаем статус "свободен" для курьера
            self.set_balance(
                self.get_balance() + job_time * 5 // 60)  # Добавляем к балансу курьера оплату за доставку заказа
            print(f'Курьер {self.__name} заработал {job_time * 5 // 60} рублей')
            self.__order_id = None  # Обнуляем идентификатор заказа

    def get_job_start(self):
        return self.__job_start

    def get_job_end(self):
        return self.__job_end

    def get_worker_id(self):
        return self.__worker_id

    def get_balance(self):
        return self.__balance

    def set_store_id(self, store_id):
        self.__store_id = store_id

    def set_balance(self, balance):
        self.__balance = balance

    def get_name(self):
        return self.__name

    def get_order_id(self):
        return self.__order_id

    def get_status(self):
        return self.__status

    def get_store_id(self):
        return self.__store_id

    def set_status(self, status):
        self.__status = status

    def __str__(self):
        return f'Курьер {self.__name} {self.__status} в магазине {self.__store_id} с {self.__job_start} до {self.__job_end}'
