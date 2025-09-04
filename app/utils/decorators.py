import time
from functools import wraps

def response_timer(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        response = await func(*args, **kwargs)
        end = time.time()
        duration = int((end - start) * 1000)  # in ms
        if isinstance(response, dict):
            response["response_time_ms"] = duration
        return response
    return wrapper
