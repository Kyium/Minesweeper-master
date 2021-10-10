from threading import Thread  # QOLFAC: quality of life functions and classes, V:1.1
from time import sleep, time as t
from sqlite3 import connect, OperationalError
from typing import Tuple, Dict, Union

class NotList(Exception):
    pass

class InvalidRange(Exception):
    pass

def integer_range_validation(inp_txt: str, ran: Tuple[int, int], inclusive: Tuple[bool, bool] = (True, True)) -> int:
    while 1:
        try:
            if ran[0] > ran[1] or (ran[0] == ran[1] and True not in inclusive):
                raise InvalidRange(f"The range: {ran} is invalid")
            integer = int(input(inp_txt + ": "))
            if ran[0] - (1 if inclusive[0] else 0) < integer < ran[1] + (1 if inclusive[1] else 0):
                return integer
            else:
                print(f"\nInput not in range, between {ran[0]} and {ran[1]}\n")
        except ValueError:
            print("\nInput was not an integer\n")


def dynamic_arg_count_function(function, args: Union[tuple, None] = None, kwargs: Union[Dict[str, any], None] = None):
    if args is not None and kwargs is not None:
        function(*args, **kwargs)
    elif args is not None and kwargs is None:
        function(*args)
    elif args is None and kwargs is not None:
        function(**kwargs)
    elif args is None and kwargs is None:
        function()


def is_empty(data):
    if isinstance(data, (tuple, list, dict)):
        if len(data) == 0:
            return True
        else:
            return False
    else:
        raise NotList


def tuple_convert(data_in):
    if isinstance(data_in, (tuple, list)):
        return data_in
    else:
        return data_in,


def function_handler(function, args: tuple = ()):
    args = tuple_convert(args)
    if args == ():
        function()
    else:
        function(*args)

def thread_run(function, args, daemonic=True):
    func = Thread(target=function, name=str(function), args=args)
    func.setDaemon(daemonic)
    func.start()

def zero(num):
    return 0 if num < 0 else num


def up_limit(num, lim):
    return num if lim > num else lim


def get_milli_time():
    return int(round(t() * 1000))


class StopWatch:
    def __init__(self):
        self.__time = 0
        self.__initial = 0
        self.__running = False

    def start(self):
        if not self.__running:
            self.__running = True
            self.__initial = get_milli_time()

    def stop(self):
        if self.__running:
            self.__time = (get_milli_time() - self.__initial) + self.__time
            self.__running = False

    def reset(self):
        if not self.__running:
            self.__time = 0
            self.__initial = 0

    def get_time(self, time_prefix="m"):
        if self.__running:
            time = (get_milli_time() - self.__initial) + self.__time
        else:
            time = self.__time
        return prefix_conversion("m", time_prefix, time)


def exec_time(func, args: tuple = None):
    stopper = StopWatch()
    stopper.start()
    if args is None:
        res = func()
    else:
        res = func(*args)
    stopper.stop()
    return res, stopper.get_time()


def prefix_conversion(current: str, required: str, data):
    p_map = {"y": -24, "z": -21, "a": -18, "f": -15, "p": -12, "n": -9, "u": -6, "m": -3, "c": -2, "d": -1,
             "b": 0, "D": 1, "H": 2, "K": 3, "M": 6, "G": 9, "T": 12, "P": 15, "E": 18, "Z": 21, "Y": 24}
    return data * (10 ** (p_map[current] - p_map[required]))


class Timer:
    def __init__(self, time, finish_com, com_args=None):
        self.original_time = time
        self.__time = self.original_time
        self.finish_command = finish_com
        self.com_args = com_args
        self.t_thread = Thread(target=self.__t_thread, name="Timer Thread (%s)" % self.original_time)
        self.t_thread.setDaemon(True)
        self.paused = False
        self.__abort = False

    def start(self):
        self.__time = self.original_time
        self.t_thread.start()

    def get_original_time(self):
        return self.original_time

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def abort(self):
        if self.__time != 0:
            self.__abort = True
            self.__time = 0

    def change_by(self, amount):
        time = self.__time + amount
        if time < 0:
            time = 0
        self.__time = time

    def set(self, amount):
        if amount < 0:
            amount = 0
        self.__time = amount

    def get_time(self):
        return self.__time

    def __t_thread(self):
        while self.__time > 0:
            if not self.paused:
                sleep(1)
                if self.__time > 0:
                    self.__time -= 1
        if not self.__abort:
            if self.com_args is None:
                self.finish_command()
            else:
                self.finish_command(*tuple_convert(self.com_args))
        else:
            self.__abort = False


if __name__ == '__main__':
    pass
