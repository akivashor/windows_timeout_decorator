import concurrent.futures as futures
from typing import Any


def timeout(timelimit: int) -> callable:
    def decorator(func: callable) -> callable:
        def decorated(*args: Any, **kwargs: Any) -> Any:
            with futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    result = future.result(timelimit)
                except futures.TimeoutError:
                    print("Timeout!")
                    executor._threads.clear()
                    futures.thread._threads_queues.clear()
                    raise TimeoutError from None

                else:
                    print(result)
                executor._threads.clear()
                futures.thread._threads_queues.clear()
                return result

        return decorated

    return decorator
