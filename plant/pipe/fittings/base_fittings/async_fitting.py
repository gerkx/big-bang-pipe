import asyncio
from random import random
from typing import Callable, Type, List

from httpx import AsyncClient
from nanoid import generate

from .fitting_state import Fitting_State
from ...fso import FSO


class Async_Fitting:
    def __init__(self, client:Type[AsyncClient]):
        self.state:Type[Fitting_State] = Fitting_State(self.broadcast)
        self.fso:Type[FSO] = FSO
        self.__guid:str = generate()
        self._subscribers:List[Callable] = []
        # self.client:Type[AsyncClient] = client
        self.client = None

    def enqueue(self):
        self.state.enqueue()
        asyncio.run(self.main())

    @property
    def guid(self):
        return self.__guid
   
    def broadcast(self):
        for callback in self._subscribers:
            callback()

    def set_parent(self, parent):
        self.fso = parent

    def subscribe(self, callback:Callable):
        if not callback in self._subscribers:
            self._subscribers.append(callback)

    async def main(self):
        while self.fso.locked:
            print("fso locked")
            asyncio.sleep(.1)
        if not self.fso.locked:
            self.client = AsyncClient()
            self.fso.lock()
            self.state.process()
            await self.fitting()
            self.fso.unlock()
            self.state.finish()

    async def fitting(self):
        dur = random()*random()
        print('override the fitting method with your own async method to be called')
        print(f'guid {self.guid} is going to sleep for {dur}')
        await asyncio.sleep(dur)
        print(f'guid {self.guid} is awake again!')

