import redis

redis_host = "localhost"
redis_port = "6379"


try:
    r = redis.StrictRedis(host=redis_host, port=redis_port)
except Exception as e:
    print(e)

def cache_results( search_parameter, texts, hash_dict ):
    if texts:
        r.rpush(search_parameter, *texts)
        r.expire(search_parameter, 10)
    if hash_dict:
        r.hmset(search_parameter + "Hashtag", hash_dict)
        r.expire(search_parameter + "Hashtag", 10)

def get_cached_results(search_parameter):

    if( r.llen(search_parameter)):
    
        return r.lrange(search_parameter, 0, -1), r.hgetall(search_parameter + "Hashtag")
    else:
        return False, False
