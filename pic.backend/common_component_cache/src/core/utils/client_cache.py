from pymemcache.client.base import Client
from pymemcache.exceptions import MemcacheIllegalInputError, MemcacheUnknownError, MemcacheUnexpectedCloseError
from typing import Optional, Any
from common_component.src.core.utils.Config import config
import json
import ssl
import ast
from common_component.src.core.utils.Logger import Log

log = Log().get_logger_service()


# ElastiCache settings

"""
A client for a single memcached server.
*Keys and Values : Keys must have a __str__() method which should return a str with no more
     than 250 ASCII characters and no whitespace or control characters.
 *Error Handling*

     All of the methods in this class that talk to memcached can throw one of
     the following exceptions:

      * :class:`pymemcache.exceptions.MemcacheClientError`
      * :class:`pymemcache.exceptions.MemcacheUnknownError`
      * :class:`pymemcache.exceptions.MemcacheIllegalInputError`
"""


class ClientCache:
    # memcache client object will hold the client.
    memcache_client = None

    """
        init will create a connection if it doesn't exit already
    """

    def __init__(self):
        if self.memcache_client is None:
            self.connect()

    """
        connect will return an object which can be used to send and receive key-value pairs from memcache

        Returns:
          memcache_client client object.
    """

    def connect(self):
        try:
            cluster_endpoint = config.MEMCACHE_CLUSTER
            context = ssl.create_default_context()
            self.memcache_client = Client(cluster_endpoint, tls_context=context)
            log.info("Connection with memcached cluster set successfully.")
        except Exception as e:
            print("this is exception -> ",e)
            log.error("Memcache cluster not available!")
            raise MemcacheUnknownError("Memcache cluster not available!")

    """
        Args:
          key: str, see class docs for details.
          default: value that will be returned if the key was not found.

        Returns:
          The value for the key, or default if the key wasn't found.
    """

    def get(self, key, default: Optional[Any] = None) -> Any:
        try:
            if self.memcache_client is None:
                self.connect()

            data = self.memcache_client.get(key)
            self.memcache_client.close()
            if data is not None:
                # Convert bytes to string
                resp = data.decode('utf-8')
                # Use ast.literal_eval to safely evaluate the string as a Python literal
                resp = ast.literal_eval(resp)
                log.info("Returning data from memcached. Key: %s", key)
                return resp
            elif default is not None:
                return default
            else:
                log.info("Given key doesn't exists in memcached. key: %s.", key)
                return "No data found"
        except Exception:
            log.debug("Something went wrong while getting the cache value for key: %s.", key)
            return "None"

    """
        Args:
          key: str, see class docs for details.
          default: value that will be returned if the key was not found.

        Returns:
          The value for the key, or default if the key wasn't found.
    """

    def router_get(self, key, default: Optional[Any] = None) -> Any:
        try:
            if self.memcache_client is None:
                self.connect()
            data = self.memcache_client.get(key)
            self.memcache_client.close()
            if data is not None:
                # Convert bytes to string
                resp = data.decode('utf-8')
                log.info("Returning data from memcached. key: %s.", key)
                return resp
            elif default is not None:
                return default
            else:
                log.info("Given key doesn't exists in memcached. key: %s.", key)
                return "No data found"
        except Exception:
            log.debug("Something went wrong while getting the cache value for key: %s.", key)
            return "None"

    """
        Args:
          key: str, If the given key exists this method will delete from memcache

        Returns:
          The value for the key, or default if the key wasn't found.
    """

    def delete(self, key):
        try:
            if self.memcache_client.get(key):
                resp = self.memcache_client.delete(key)
                self.memcache_client.close()
                log.info("Given key got deleted from memcached. Key: %s", key)
                return resp
        except Exception:
            log.debug("Given key not found in memcached. key: %s.", key)
            raise MemcacheIllegalInputError("Key not found: %r" % key)

    """
        Args:
          key: str. Key for accessing data from memcache
          value: str. Actual data which we need to store in the memcache 
          expire: time in seconds. Till we want key value to be available in the memcache

        New key properties:
        1. Should be less than 250  char
        2. Shouldn't be a null value
    """

    def set(self, key: str, value: str, expire: int = 0):
        if len(key) > 250:
            raise MemcacheIllegalInputError("Key is too long: %r" % key)
        elif key is None:
            raise MemcacheIllegalInputError("Key contains null: %r" % key)
        try:
            if self.memcache_client is None:
                self.connect()
            if (key is not None) and (len(key) < 250):
                response = self.memcache_client.set(key, value.encode(encoding="ascii", errors="backslashreplace"),
                                                    expire=expire)
                response_data = self.memcache_client.get(key, "None")
                self.memcache_client.close()
                log.info("Data for given key set successfully in memcached. key: %s", key)
                return response
        except Exception as e:
            log.debug("Something went wrong %r", e)
            return "None"


    """
        Delete all the keys in memcache
    """
    def delete_all(self):
        try:
            if self.memcache_client is None:
                self.connect()
            self.memcache_client.flush_all()
            self.memcache_client.close()
            log.info("All memcached keys got deleted successfully")
        except Exception:
            log.debug("Something went wrong while deleting all memcached keys")
            raise MemcacheUnexpectedCloseError("Something went wrong while deleting all keys")

