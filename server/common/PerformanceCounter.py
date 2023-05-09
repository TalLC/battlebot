import asyncio
from time import time, sleep
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict
from common.Singleton import SingletonABCMeta

from threading import Thread, Event as ThreadEvent

from contextlib import contextmanager
import functools

# Monitoring a whole file:
# while [ 1 ]; do clear; printf 'Current time:\t%(%d/%m/%Y %H:%M:%S)T\n'; cat perfs.log; sleep 1 ;done


class Counter:

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def last_time(self) -> timedelta:
        return self._last_time

    @property
    def average_time(self) -> timedelta:
        return self._added_times / self._iterations

    @property
    def total_time(self) -> timedelta:
        return self._added_times

    @property
    def iterations(self) -> int:
        return self._iterations

    def __init__(self, func, uid: str):
        self._function = func
        self._uid = uid
        self._last_time = timedelta()
        self._added_times = timedelta()
        self._iterations = 0

    def update(self, value: timedelta):
        self._last_time = value
        self._added_times += value
        self._iterations += 1

    def stats(self) -> str:
        return f"Function: {self._function.__qualname__} (x{self.iterations})\n" \
               f"Last time: {self.last_time}\n" \
               f"Avg time: {self.average_time}\n" \
               f"Total time: {self.total_time}"


class PerformanceCounter(metaclass=SingletonABCMeta):
    _COUNTERS: Dict[str, Counter] = dict()
    _REPORT_FILE: Path = Path('perfs.log')

    def __init__(self):
        self._REPORT_FILE.write_text('')
        self._start_time = datetime.now()
        self._reporting_thread_event = ThreadEvent()
        self._reporting_thread = Thread(
            target=self._thread_reporting,
            args=(self._reporting_thread_event, 5000)
        ).start()

    def stop(self):
        self._reporting_thread_event.set()

    def register_counter(self, func):
        func_hash = PerformanceCounter.get_func_uid(func)
        self._COUNTERS[func_hash] = Counter(func, func_hash)

    def update_counter(self, func, value: timedelta):
        func_hash = PerformanceCounter.get_func_uid(func)
        if func_hash not in self._COUNTERS:
            self.register_counter(func)
        self._COUNTERS[func_hash].update(value)

    def report(self) -> str:
        counters = sorted(self._COUNTERS.values(), key=lambda c: c.iterations, reverse=True)
        stats = '\n\n'.join([c.stats() for c in counters])
        return f"Started at:\t{self._start_time.strftime('%d/%m/%Y %H:%M:%S')}\n"\
               f"===================================\n"\
               f"{stats}"

    def write_report(self):
        self._REPORT_FILE.write_text(data=self.report(), encoding='utf-8')

    def show_report(self):
        print(self.report())

    @staticmethod
    def get_func_uid(func) -> str:
        return hex(func.__hash__())[2:]

    @staticmethod
    def decorate_sync_async(decorating_context, func):
        if asyncio.iscoroutinefunction(func):
            async def decorated(*args, **kwargs):
                with decorating_context():
                    return await func(*args, **kwargs)
        else:
            def decorated(*args, **kwargs):
                with decorating_context():
                    return func(*args, **kwargs)

        return functools.wraps(func)(decorated)

    @staticmethod
    @contextmanager
    def wrapping_logic(func):
        start_ts = time()
        yield
        PerformanceCounter().update_counter(
            func,
            timedelta(seconds=time() - start_ts)
        )

    @staticmethod
    def count(func):
        timing_context = lambda: PerformanceCounter().wrapping_logic(func)
        return PerformanceCounter().decorate_sync_async(timing_context, func)

    def _thread_reporting(self, e: ThreadEvent, interval_ms: int):
        while not e.is_set():
            sleep(interval_ms / 1000)
            if len(self._COUNTERS.keys()):
                self.write_report()
