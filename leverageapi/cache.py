from flask import request
from flask.ext.cache import Cache
from leverageapi.app_config import CACHE_CONFIG

def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    # print 'cache_key:', (path+args)
    return (path + args)

cache = Cache(config=CACHE_CONFIG)
CACHE_TIMEOUT = 60*60*6


