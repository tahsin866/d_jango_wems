import redis
import json
from django.conf import settings

def get_redis_client():
    return redis.StrictRedis.from_url(settings.REDIS_URL)

def cache_user_auth(key, data, expire=3600):
    client = get_redis_client()
    client.setex(key, expire, json.dumps(data))

def get_cached_user_auth(key):
    client = get_redis_client()
    cached = client.get(key)
    if cached:
        return json.loads(cached)
    return None
