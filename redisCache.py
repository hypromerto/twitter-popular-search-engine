import redis

redis_host = "localhost"
redis_port = "6379"
redis_password = "galata25"


try:
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)
except Exception as e:
    print(e)

def cacheResults( search_parameter, texts, hashDict ):
    if texts:
        r.lpush(search_parameter, *texts)
        r.expire(search_parameter, 5)
    if hashDict:
        r.hmset(search_parameter + "Hashtag", hashDict)
        r.expire(search_parameter + "Hashtag", 5)

def getCachedResults(search_parameter):

    if( r.hlen(search_parameter)):
        return r.lrange(search_parameter, 0, -1), r.hgetall(search_parameter + "Hashtag")
    else:
        return False, False
