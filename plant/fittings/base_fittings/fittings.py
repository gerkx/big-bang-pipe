from typing import Callable

from .fitting_state import Fitting_State


class Fitting:
    def __init__(self, queue:object, fso:object, **kwargs):
        self.state:object = Fitting_State()
        self.queue:object = queue
        self.fso:object = fso
        self.kwargs:dict = {**kwargs}

    def enqueue(self):
        self.queue.add(self.main)
        self.state.enqueue()

    def main(self):
        self.state.process()
        self.fitting()
        self.state.finish

    def fitting(self):
        print("overwrite this method with fitting method")

class Async_Fitting(Fitting):

    async def enqueue(self):
        await self.queue.add(self.main)
        self.state.enqueue