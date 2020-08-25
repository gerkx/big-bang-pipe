from typing import Callable, Type

from nanoid import generate
from box import Box

from .fitting_state import Fitting_State

from ...fso import FSO

from ....queues import Queue


class Fitting:
    def __init__(self, queues:Type[Queue]):
        self.state:object = Fitting_State(self.broadcast)
        self.queue:object = queues.io
        self.fso:Type[FSO] = FSO
        self.guid:str = generate()
        self._subscribers:list = []

    def enqueue(self):
        self.state.enqueue()
        self.queue.add(self.main)

    def main(self):
        if not self.fso.locked:
            self.fso.lock()
            self.state.process()
            self.fitting()
            self.state.finish()
            self.fso.unlock()

    def subscribe(self, callback:Callable):
        if not callback in self._subscribers:
            self._subscribers.append(callback)

    def set_parent(self, parent):
        self.fso = parent

    def broadcast(self):
        for callback in self._subscribers:
            callback()

    def fitting(self):
        print("overwrite the fitting method with your own instructions!")


class Async_Fitting(Fitting):
    def __init__(self, queues:object):
        super().__init__(queues)
        self.queue = queues.aio

    async def enqueue(self):
        await self.queue.add(self.main)
        self.state.enqueue

    async def main(self):
        if not self.fso.locked:
            self.fso.lock()
            self.state.process()
            await self.fitting()
            self.state.finish()
            self.fso.unlock()
    
    def fitting(self):
        print("overwrite the fitting method with your own async/await instructions!")


class CPU_Fitting(Fitting):
    def __init__(self, queues:object):
        super().__init__(queues)
        self.queue = queues.cpu