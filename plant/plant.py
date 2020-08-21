import time
from threading import Thread

class Plant:
    def __init__(self, 
        pipe_list:list, 
        poll_freq:float = 1.0, 
        number_of_threads:int = 1
    ):
        self.pipes = pipe_list
        self._frequency = poll_freq
        self.number_of_threads = number_of_threads
        self.__active = True
        self._threads:list = self.threaded_poll

    def threaded_poll(self):
        thread_ids = []
        for _ in range(self.number_of_threads):
            thread = Thread(target=self.poll)
            thread.start()
            thread_ids.append(thread.native_id)
        return thread_ids

    def poll(self):
        while self.__active:
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
        return self.__active

    def activate(self):
        self.__active = True
    
    def deactivate(self):
        self.__active = False

