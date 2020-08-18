import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""

redisIns = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)