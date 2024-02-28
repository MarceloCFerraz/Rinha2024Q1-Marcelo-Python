import time

import init

import init


class Enqueuer:
    def __init__(self) -> None:
        i = 0
        while True:
            i += 1
            init.queue.append(init.task, f"Task {i}")
            time.sleep(0.8)
