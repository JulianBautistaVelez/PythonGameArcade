def run_async(func):
    from threading import Thread
    from functools import wraps

    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl

    return async_func


def log_timer(func):
    import time
    from functools import wraps

    @wraps(func)
    def log_func(*args, **kwargs):
        start_time = time.time()
        result = func(*args)
        exc_time = time.time() - start_time
        print("the function {} ran in {} seconds".format(func.__name__, exc_time))

        return result
    return log_func

