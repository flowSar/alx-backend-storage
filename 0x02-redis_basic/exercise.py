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
