#!/usr/bin/env python3
""" Cache class """
import redis
from uuid import uuid4
from typing import Union
from functools import wraps


def count_calls(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(inputs_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, output)

        return output
    return wrapper


class Cache:
    """Cache class to write strings to Redis"""
    def __init__(self):
        """Initialization"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method genrates a random key"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key, fn=None):
        """Convert the data back to the desired format"""
        val = self._redis.get(key)
        if val is None:
            return None
        if fn:
            return fn(val)
        return val

    def get_str(self, key):
        """Automatically parametrize Cache.get to str"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key):
        """Automatically parametrize Cache.get to int"""
        return self.get(key, fn=int)

    def replay(method: Callable):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        inputs = cache._redis.lrange(inputs_key, 0, -1)
        outputs = cache._redis.lrange(outputs_key, 0, -1)

        print(f"{method.__qualname__} was called {len(inputs)} times:")
        for args, output in zip(inputs, outputs):
            print(f"{method.__qualname__}\
            (*{args.decode()}) -> {output.decode()}")
