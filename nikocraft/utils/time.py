"""Interface for standard modules time and datetime"""

# Standard modules
import time as _time
import datetime as _datetime
from typing import Callable


def wait(duration: float) -> None:
    """Wait for a specific amount of seconds"""
    _time.sleep(duration)


def epoch_start() -> _time.struct_time:
    """Get the datetime the epoch started"""
    return _time.gmtime(0)


def epoch_time() -> float:
    """Get the time in seconds since the epoch (Get epoch start with epoch_start())"""
    return _time.time()


def epoch_time_ns() -> int:
    """Get the time in nanoseconds since the epoch (Get epoch start with epoch_start())"""
    return _time.time_ns()


def bench_time() -> float:
    """Get a time in seconds for calculating a duration by getting the difference"""
    return _time.perf_counter()


def bench_time_ns() -> int:
    """Get a time in nanoseconds for calculating a duration by getting the difference"""
    return _time.perf_counter_ns()


def run_time() -> float:
    """Get the time in seconds since the process started"""
    return _time.process_time()


def run_time_ns() -> int:
    """Get the time in nanoseconds since the process started"""
    return _time.process_time_ns()


def time_f_hms() -> str:
    """Get the time as a string in the format H:M:S"""
    return _datetime.datetime.now().strftime("%H:%M:%S")


def date_f_dmy() -> str:
    """Get the date as a string in the format D.M.Y"""
    return _datetime.datetime.now().strftime("%d.%b.%y")


def datetime_f_dmy_hms() -> str:
    """Get the datetime as a string in the format D.M.Y H:M:S"""
    return _datetime.datetime.now().strftime("%d.%b.%y %H:%M:%S")


def datetime_f_ymd_hms() -> str:
    """Get the datetime as a string in the format Y-M-D_Hh-Mm-Ss"""
    return _datetime.datetime.now().strftime("%Y-%m-%d_%Hh-%Mm-%Ss")


def datetime_f(datetime_format: str) -> str:
    """Get the datetime as a string in a custom format"""
    return _datetime.datetime.now().strftime(datetime_format)


def benchmark() -> Callable[[], float]:
    """Start benchmark"""

    start = bench_time()

    def stop() -> float:
        """Stop benchmark"""
        return bench_time() - start

    return stop
