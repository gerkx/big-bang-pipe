from .async_queue import ASYNC_Queue
from .fifo_queue import FIFO_Queue

class Queue():
    def __init__(self):
        self.io = FIFO_Queue()
        self.aio = ASYNC_Queue()
        self.cpu = FIFO_Queue(number_of_threads=1)