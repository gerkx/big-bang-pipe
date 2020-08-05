import time

class Plant:
    def __init__(self, pipe_list:list, poll_freq:int = 1):
        self.pipes = pipe_list
        self._frequency = poll_freq
        self.__active = True

    async def poll(self):
        while self.__active:
            for pipe in self.pipes:
                pipe.poll()
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

    @active.setter
    def active(self, val):
        self.__active = val

