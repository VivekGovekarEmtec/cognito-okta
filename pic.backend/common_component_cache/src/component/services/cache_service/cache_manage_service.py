from common_component.src.core.utils.client_cache import ClientCache
import os
import json


def set_cached_data(key: str, value: str, expire: int = 0):
    """
    key will be key of the cache. Value is the actual content needs to be cached
    expire is the timeperiod in sec we want value to be cached
    :param expire: timeperiod for which we want keep this key in cache
    :param value: actual value we want to store in cache
    :param key: key: string
                value: string
                expire: int
    :return:
    """
    try:
        client = ClientCache()
        response = client.set(key, str(value), expire)
        return response
    except Exception as e:
        print(e)
        error_message = f"Error while pushing data for the given key : {str(e)}"
        return error_message


def get_cached_data(key: str, default: str):
    """
    return the content from cache based on given key. If not found, will return the default value
    :param default: Default string which will be returned if key doesn't exist
    :param key: key: string
                default: string
    :return: response: string
    """
    try:
        client = ClientCache()
        data = client.get(key, default)
        response_data = json.loads(json.dumps(data, default=str))
        response = {
            "status_code": 200,
            "message": "Received cache data from memcached successfully",
            "data": {key: response_data}
        }
        return response

    except Exception as e:
        print(e)
        error_message = f"Error while getting data for the given key : {str(e)}"
        raise error_message


def delete_cache_key(key: str):
    """
        This function will delete given key from memcache
    """
    try:
        client = ClientCache()
        client.delete(key=key)
        return "Key deleted successfully"
    except Exception as e:
        print(e)
        error_message = f"Error while deleting data for the given key : {str(e)}"
        return error_message


def delete_all_cache_key():
    """
        This function will clean memcache
    """
    try:
        client = ClientCache()
        client.delete_all()
        return "All keys deleted successfully"
    except Exception as e:
        print(e)
        error_message = f"Error while cleaning memcache : {str(e)}"
        return error_message


