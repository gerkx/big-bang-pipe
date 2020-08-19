from queue import Queue
from threading import Thread

class FIFO_Queue:
    def __init__(self, number_of_threads:int = 8):
        self.sync:bool = True    
        self._queue:object = Queue()
        self.number_of_threads:int = number_of_threads
        self._threads:list = self.threaded_workers()
        # print(self._threads)

    def worker(self):
        while True:
        # while not self._queue.empty():
            task = self._queue.get()
            task()
            self._queue.task_done()

    def spawn(self):
        if len(self._threads) < self.number_of_threads:
            thread = Thread(target=self.worker)
            thread.start()
            self._threads.append(thread.native_id)

    def threaded_workers(self):
        thread_ids = []
        for _ in range(self.number_of_threads):
            thread = Thread(target=self.worker)
            # thread.daemon = True
            thread.start()
            thread_ids.append(thread.native_id)
        return thread_ids

    def add(self, *tasks):
        for task in tasks:
            self._queue.put_nowait(task)
            # self.spawn()
            # print(self._threads)
            # print(self._queue.qsize())
