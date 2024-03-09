import threading
import time
from queue import Queue

# Глобальный лок для синхронизации вывода в консоль
print_lock = threading.Lock()

class CustomThread(threading.Thread):
    """
    Класс CustomThread, наследуемый от threading.Thread.
    Позволяет создавать потоки с дополнительными функциями, такими как возможность завершения потока,
    ограничение времени выполнения и использование очереди для передачи данных между потоками.
    """

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, Verbose=None, flag=None, timers=None):
        """
        Инициализация потока.

        :param group: Группа потоков.
        :param target: Целевая функция для выполнения в потоке.
        :param name: Имя потока.
        :param args: Аргументы для целевой функции.
        :param kwargs: Именованные аргументы для целевой функции.
        :param Verbose: Флаг для подробного вывода.
        :param flag: Флаг для ограничения времени выполнения.
        :param timers: Время ожидания выполнения потока.
        """
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
        self._is_killed = False
        self.start_time = None
        self.flag = flag
        self.timers = timers

    def kill(self):
        """
        Метод для завершения потока.
        """
        self._is_killed = True

    def run(self):
        """
        Переопределенный метод run для запуска потока.
        Выполняет целевую функцию с ограничением времени выполнения, если флаг установлен.
        """
        if self._is_killed:
            return
        if self._target is not None:
            if self.flag:
                self.start_time = time.perf_counter()
                self._return = self._target(*self._args, **self._kwargs)
                while True:
                    if self._is_killed or time.perf_counter() - self.start_time >= self.timers:
                        self.kill()
                        break
            else:
                self._return = self._target(*self._args, **self._kwargs)

    def join(self, timeout=None):
        """
        Переопределенный метод join для ожидания завершения потока.
        Возвращает результат выполнения целевой функции.

        :param timeout: Таймаут ожидания завершения потока.
        :return: Результат выполнения целевой функции.
        """
        threading.Thread.join(self, timeout=timeout)
        return self._return


def thread(func):
    """
    Декоратор для создания потока без ограничения времени выполнения.

    :param func: Целевая функция для выполнения в потоке.
    :return: Функция-обертка, которая создает и запускает поток.
    """
    def wrapper(*args, **kwargs):
        my_thread = CustomThread(target=func, args=args, kwargs=kwargs)
        my_thread.start()
        return my_thread

    return wrapper


def thread2(flag, timer):
    """
    Декоратор для создания потока с ограничением времени выполнения.

    :param flag: Флаг для включения ограничения времени выполнения.
    :param timer: Время ожидания выполнения потока.
    :return: Функция-обертка, которая создает и запускает поток с ограничением времени.
    """
    def decor(func):
        def wrapper(*args, **kwargs):
            my_thread = CustomThread(target=func, args=args, kwargs=kwargs, flag=flag, timers=timer)
            my_thread.start()
            return my_thread
        return wrapper
    return decor


def thread3(use_queue=False, queue_size=None):
    """
    Декоратор для создания потока с использованием очереди для передачи данных.

    :param use_queue: Флаг для использования очереди.
    :param queue_size: Максимальный размер очереди.
    :return: Функция-обертка, которая создает и запускает поток с очередью.
    """
    def decor(func):
        def wrapper(*args, **kwargs):
            if use_queue:
                queue = Queue(queue_size)
                my_thread = CustomThread(target=func, args=(queue,) + args, kwargs=kwargs)
                my_thread.start()
                return my_thread
            else:
                my_thread = CustomThread(target=func, args=args, kwargs=kwargs)
                my_thread.start()
                return my_thread
        return wrapper
    return decor


def threaClass(func):
    """
    Декоратор для создания потока с использованием класса CustomThread.

    :param func: Целевая функция для выполнения в потоке.
    :return: Функция-обертка, которая создает и запускает поток.
    """
    def wrapper(*args, **kwargs):
        my_thread = CustomThread(target=func, args=args, kwargs=kwargs)
        my_thread.start()
        return my_thread
    return wrapper
