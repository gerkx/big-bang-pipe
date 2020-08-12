from typing import Callable

from nanoid import generate

from .fitting_state import Fitting_State


class Fitting:
    def __init__(self, queue:object):
        self.state:object = Fitting_State(self.broadcast)
        self.queue:object = queue
        self.fso:object = None
        # self.kwargs:dict = {**kwargs}
        self.guid:str = generate()
        self._subscribers:list = []

    def enqueue(self):
        self.state.enqueue()
        self.queue.add(self.main)

    def main(self):
        self.state.process()
        self.fitting()
        self.state.finish()

    def subscribe(self, callback:Callable):
        if not callback in self._subscribers:
            self._subscribers.append(callback)

    def parent(self, parent):
        self.fso = parent

    def broadcast(self):
        for callback in self._subscribers:
            callback()

    def fitting(self):
        print("overwrite this method with fitting method")


class Async_Fitting(Fitting):

    async def enqueue(self):
        await self.queue.add(self.main)
        self.state.enqueue