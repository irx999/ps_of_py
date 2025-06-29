import time

from src.logger import Logger

logger = Logger(
    __name__,
    log_name="time.log",
)


def timer(threshold=None):
    """装饰器_记录程序运行时间"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"{func.__name__} 运行了 {end_time - start_time} 秒")
            spend_time = end_time - start_time
            if threshold is not None:
                if spend_time > threshold:
                    logger.debug("%s took %s    seconds", func.__name__, spend_time)
            logger.info("%s took %sseconds", func.__name__, spend_time)
            return result

        return wrapper

    return decorator
