import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def cache_feed(user_id, posts):
    key = f"feed:{user_id}"
    r.set(key, json.dumps([p.id for p in posts]), ex=60)

def get_cached_feed(user_id):
    key = f"feed:{user_id}"
    ids = r.get(key)
    if ids:
        return json.loads(ids)
    return None