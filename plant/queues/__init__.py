from .async_queue import ASYNC_Queue
from .fifo_queue import FIFO_Queue

class Queue():
    def __init__(self):
        self.fifo = FIFO_Queue()
        self.aio = ASYNC_Queue()