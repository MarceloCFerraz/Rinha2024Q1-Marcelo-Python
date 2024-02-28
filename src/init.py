import time

import gevent.monkey
from Pool.thread_pool import ThreadPool
from Server.http_server import HTTPServer

gevent.monkey.patch_all()  # Ensure monkeypatching


def cpu_intensive_task(arg1, arg2):
    # Simulate a long-running CPU operation
    result = 0
    for i in range(500):
        result += arg1 * arg2
        if i % 20 == 0:
            time.sleep(0.5)  # chance for yielding back to other threads
    return result


def task(message):
    print(message)
    time.sleep(5)


if __name__ == "__main__":
    pool = ThreadPool()
    server = HTTPServer(pool)

    # Main thread can enqueue tasks
    # for i in range(1, 50):
    #     print("Enqueuing item")
    #     task_queue.put(item=(task, f"Task {i}"))
    # ... Enqueue more tasks
    # asyncio.run(run_server())
    # task_queue.join()
