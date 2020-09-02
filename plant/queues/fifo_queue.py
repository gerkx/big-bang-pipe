from queue import Queue
from threading import Thread, Event
import time

class FIFO_Queue:
    def __init__(self, number_of_threads:int = 8):
        self.__active = True
        self._queue:object = Queue()
        self.number_of_threads:int = number_of_threads
        self._threads:list = self.threaded_workers()


    def activate(self):
        if not self.active:
            self._threads = self.threaded_workers()
            self.__active = True

    def deactivate(self):
        for _ in self._threads:
            self.add(None)
        for thread in self._threads:
            thread.join()
        self.__active = False

    @property
    def active(self) -> bool:
        return self.__active

    def worker(self):
        while True:
            time.sleep(.001)
            task = self._queue.get()
            if task is None:
                break
            task()
            self._queue.task_done()

    def threaded_workers(self):
        threads = []
        for _ in range(self.number_of_threads):
            thread = Thread(target=self.worker)
            # thread.daemon = True
            thread.start()
            threads.append(thread)
        return threads

    def add(self, *tasks):
        for task in tasks:
            self._queue.put_nowait(task)
