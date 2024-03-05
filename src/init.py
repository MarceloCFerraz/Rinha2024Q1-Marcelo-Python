from Server.Pool.thread_pool import ThreadPool
from Server.server import HTTPServer

if __name__ == "__main__":
    pool = ThreadPool()
    server = HTTPServer(pool)
    # http server running on the main thread will enqueue requests

    # Main thread can enqueue tasks
    # for i in range(1, 50):
    #     print("Enqueuing item")
    #     task_queue.put(item=(task, f"Task {i}"))
    # ... Enqueue more tasks
    # asyncio.run(run_server())
    # task_queue.join()
