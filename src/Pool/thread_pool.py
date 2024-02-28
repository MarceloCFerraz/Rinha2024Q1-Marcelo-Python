import os
import threading

import gevent
import gevent.monkey
from gevent import queue

gevent.monkey.patch_all()  # Ensure monkeypatching


class ThreadPool:
    MAX_WORKERS: int
    MAX_FIBERS: int
    connection_queue: queue.Queue

    def __init__(self, max_workers=None, max_fibers=None):
        self.MAX_WORKERS = (
            max_workers
            if max_workers is not None
            else int(os.getenv("MAX_WORKERS"))
            if os.getenv("MAX_WORKERS")
            else 10
        )
        self.MAX_FIBERS = (
            max_fibers
            if max_fibers is not None
            else int(os.getenv("MAX_FIBERS"))
            if os.getenv("MAX_FIBERS")
            else 10
        )
        self.connection_queue = queue.Queue(self.MAX_WORKERS * self.MAX_FIBERS)
        self.start_thread_pool()

    def start_thread_pool(self):
        print(f">> Initializing {self.MAX_WORKERS} worker threads")
        for _ in range(self.MAX_WORKERS):
            threading.Thread(target=self.start_worker).start()

    def start_worker(self):
        self.fetch_for_connections()

    def fetch_for_connections(self):
        # greent.get_hub().threadpool.size:
        while True:
            try:
                work, *args = self.connection_queue.get(block=True, timeout=0.1)
                # print(">> dequeuing item")
                gevent.spawn(work, *args)
            except queue.Empty:
                pass
                # print(">> queue empty")
                # time.sleep(1) # not needed, because dequeue already waits for 100 ms

    def get_backlog_length(self):
        return self.MAX_FIBERS * self.MAX_WORKERS

    def add_connection_to_queue(self, item):
        try:
            # raises `queue.Full` exception if no free slot is immediately available
            self.connection_queue.put(item, block=False)
        except queue.Full:
            # add the connection to a pending connections queue
            pass
