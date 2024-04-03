#!/usr/bin/env python3
"""
Module for making request for Redis
"""
import requests
from functools import wraps
from redis import Redis
from typing import Callable, Optional

# Redis connection details (adjust if needed)
REDIS_HOST = "localhost"
REDIS_PORT = 6379

# Cache expiration time in seconds
CACHE_EXPIRY = 10

# Redis client
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT)

def access_count(func: Callable) -> Optional[Callable]:
    """
    Function for wrapping get_page
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Optional[str]:
        """
        FUnction to cache the number of times a url is accessed
        """
        cache_key = f"count:{args[0]}"

        url_text, status_code = func(*args, **kwargs)
        print('url test: ', url_text, 'status code: ', status_code)
        if url_text and status_code == 200:
            redis_client.incr(cache_key)
            redis_client.expire(cache_key, CACHE_EXPIRY)
            value = redis_client.get(cache_key)
            return value
        else:
            print("Request to url failed")
            return

    return wrapper

@access_count
def get_page(url: str) -> Optional[tuple]:
    """
    Fetches the HTML content of a URL using requests.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception:
        pass
    return response.text, response.status_code


if __name__ == "__main__":
    pass
