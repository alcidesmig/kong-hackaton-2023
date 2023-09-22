import hashlib
import os
import pickle

import redis
from src.cache.repository import ICacheRepository


class RedisRepository(ICacheRepository):
    def __init__(self):
        self.client: redis.Redis = redis.Redis.from_url(
            url=os.getenv('REDIS_CONNECTION_URI', 'redis://localhost:6379/1'), password=os.getenv('REDIS_PASSWORD', '123456')
        )

    def _encode(self, text):
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def get(self, key):
        try:
            # Encode key
            key = self._encode(key)
            # Get from redis
            obj = self.client.get(key)

            if obj is None:
                return None
            return pickle.loads(obj)
        except Exception:
            # @TODO log
            return None

    def set_(self, key, value, exp_time_seconds):
        try:
            # Encode key
            key = self._encode(key)
            # Set data
            self.client.setex(key, exp_time_seconds, pickle.dumps(value))
        except Exception:
            # @TODO log
            return None


def get_cache_repository() -> ICacheRepository:
    return RedisRepository()
