import functools
from health_check.logging import current_logger as logger


def connection_cache(func):
    _cache = None

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal _cache
        if not _cache:

            def _generator(*args, **kwargs):
                host, port, *_ = args
                client = func(*args, **kwargs)
                try:
                    while True:
                        yield client
                # close when system terminate
                except:  # noqa E722
                    if hasattr(client, "close"):
                        client.close()
                    logger.debug("[%s:%s] close: ok", host, port)

            _cache = _generator(*args, **kwargs)
            return _cache.__next__()
        else:
            return _cache.__next__()

    return wrapper
