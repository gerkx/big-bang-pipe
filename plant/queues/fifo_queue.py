from queue import Queue
from threading import Thread

class FIFO_Queue:
    def __init__(self, number_of_threads:int = 1):
        self.sync:bool = True    
        self._queue:object = Queue()
        self._threads:list = self.threaded_workers()
        self.number_of_threads:int = number_of_threads

    def worker(self):
        while not self._queue.empty():
            task = self._queue.get()
            task()
            self._queue.task_done()

    def threaded_workers(self):
        thread_ids = []
        for _ in range(self.number_of_threads):
            thread = Thread(target=self.worker)
            thread.start()
            thread_ids.append(thread.native_id)
        return thread_ids

    def add(self, *tasks):
        for task in tasks:
            self._queue.put(task)