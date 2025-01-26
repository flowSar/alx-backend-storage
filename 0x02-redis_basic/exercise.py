#!/usr/bin/env python3
"""module fo dealing with redis"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(func: Callable) -> Callable:
    """Decorator to count the number of calls to a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.store += 1
        return func(*args, **kwargs)
    wrapper.store = 0
    return wrapper


def call_history(method: Callable) -> Callable:
    """call_history"""
    inkey = method.__qualname__ + ":inputs"
    outkey = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper"""
        self._redis.rpush(inkey, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(outkey, str(res))
        return res

    return wrapper


def replay(method: Callable) -> None:
    """replay"""
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(inputs)))
    for inp, out in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(
                method.__qualname__, inp.decode("utf-8"), out.decode("utf-8")
            )
        )


class Cache:
    """Cache class"""

    def __init__(self):
        """create redis object"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store data with a generated key to the redis
        and return the key of data"""
        key = str(uuid.uuid4())
        if isinstance(data, (uuid.UUID)):
            data = str(data)
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> str:
        """retreive data from redis"""
        data = self._redis.get(key)
        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> str:
        """get data format str"""
        data = self._redis.get(str)
        return str(data)

    def get_int(self, key: str) -> int:
        """get data format int"""
        data = self._redis.get(str)
        return int(data)
