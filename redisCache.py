import redis

redis_host = "localhost"
redis_port = "6379"
redis_password = "galata25"


try:
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)
except Exception as e:
    print(e)

def cacheResults( search_parameter, results ):
    r.hmset(search_parameter, results)
    r.expire(search_parameter, 5)

def getCachedResults(search_parameter):

    if( r.hlen(search_parameter)):
        return r.hgetall(search_parameter)
    else:
        return False
