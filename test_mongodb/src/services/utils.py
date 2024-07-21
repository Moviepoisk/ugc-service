import random
import string
import time
from functools import wraps


def random_string(length=10):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))


def speedtest(f):
    @wraps(f)
    async def wrap(*args, **kwargs):
        start_time = time.time()
        result = await f(*args, **kwargs)
        end_time = time.time()
        print(f"Function {f.__name__} took {end_time - start_time:.4f} seconds")
        return result

    return wrap
