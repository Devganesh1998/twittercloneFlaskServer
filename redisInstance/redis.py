import redis
from redisInstance.credentials import redisHost

# redis_host = redisHost or "localhost"
redis_host = "localhost"
redis_port = 6379
redis_password = ""

pool = redis.ConnectionPool(host=redis_host, port=redis_port)
redisIns = redis.Redis(connection_pool=pool)

# redisIns = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)