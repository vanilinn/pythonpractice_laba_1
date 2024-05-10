from abc import ABC, abstractmethod

from order import Order


class Worker(ABC):
    def __init__(self, worker_id, name):
        self.__worker_id = worker_id
        self.__name = name
        self.__store_id = None
        self.__job_start = None
        self.__job_end = None
        self.__status = 'свободен'
        self.__order_id = None
        self.__balance = 0

    @abstractmethod
    def get_order(self, store, order: Order):
        pass

    # принять заказ, если возможно

    @abstractmethod
    def get_shift(self, job_time, store):
        pass

    # получить смену, когда работает

    @abstractmethod
    def get_status(self):
        pass

    @abstractmethod
    def set_status(self, status):
        pass

    @abstractmethod
    def get_worker_id(self):
        pass

    @abstractmethod
    def get_order_id(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_store_id(self):
        pass

    @abstractmethod
    def get_balance(self):
        pass

    @abstractmethod
    def set_balance(self, balance):
        pass

    @abstractmethod
    def set_store_id(self, store_id):
        pass

    @abstractmethod
    def __str__(self):
        return f'Работник {self.__name} {self.__status} в магазине {self.__store_id} с {self.__job_start} до {self.__job_end}'
