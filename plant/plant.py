import time
from typing import List, Type
from threading import Event, Thread

from .pipe import init_Pipe, Pipe
from .queues import Queue

class Plant:
    def __init__(self,
        queues: Type[Queue],
        pipe_configs:List[dict], 
        poll_freq:float = 1.0, 
        number_of_threads:int = 1
    ):
        self.pipes:List[Pipe] = self.init_pipes(queues, pipe_configs)
        self.queues:Type[Queue] = queues
        self._frequency:float = poll_freq
        self.number_of_threads:int = number_of_threads
        self.__shutdown:Type[Event] = Event()
        self._threads:List[Thread] = self.threaded_poll()

        self.start()

    def start(self):
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.deactivate()

    def init_pipes(self, queues:Type[Queue], pipe_configs:List[dict]) -> List[dict]:
        return [init_Pipe(queues, **config) for config in pipe_configs]
    
    def threaded_poll(self):
        threads = []
        for _ in range(self.number_of_threads):
            thread = Thread(target=self.poll)
            thread.start()
            threads.append(thread)
        return threads

    def poll(self):
        while True:
            if self.__shutdown.is_set():
                break
            for pipe in self.pipes:
                pipe.update()
            time.sleep(self._frequency)

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, val):
        self._frequency = val

    @property
    def active(self):
        return False if self.__shutdown.is_set() else True

    def activate(self):
        self.__shutdown.clear()

    
    def deactivate(self):
        self.__shutdown.set()
        for thread in self._threads:
            thread.join()
        self.queues.io.deactivate()

