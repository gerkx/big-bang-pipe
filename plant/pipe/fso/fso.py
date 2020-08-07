import os
from os import path
from typing import Type

from .fso_state import FSO_State
from .fso_available import fso_is_available

async def create_FSO(path, q):
    fso = FSO(path, [], q)
    await fso.q.add((fso, 'available'))
    return fso

class FSO:
    def __init__(self, path:str, fittings:list, q):
        self.__path:str = path
        self.state:Type[FSO_State] = FSO_State(fittings)
        self._subscribers:list = []
        self.q = q

        self.state.subscribe(self.hollaback)



    def subscribe(self, callback):
        self._subscribers.append(callback)

    def broadcast(self):
        for sub in self._subscribers:
            sub(self.__path)

    async def available(self):
        await fso_is_available(self.path, self.state.ready)
        # while self.state == 'pending':

    @staticmethod
    def hollaback():
        print('hollllaaaaaa')
        return

    # path property
    @property
    def path(self) -> str:
        return self.__path
    @path.setter
    def path(self, val:str):
        self.__path = val
        self.broadcast()


    # filename property
    @property
    def filename(self) -> str:
        return path.basename(self.__path)
    @filename.setter
    def filename(self, val:str):
        self.__path = path.join(path.dirname(self.__path), val)
        self.broadcast()


    # directory property
    @property
    def directory(self) -> str:
        return path.dirname(self.__path)
    @directory.setter
    def directory(self, val:str):
        self.__path = path.join(val, self.filename)
        self.broadcast()


    # name property
    @property
    def name(self) -> str:
        return path.splitext(path.basename(self.__path))[0]
    @name.setter
    def name(self, val:str):
        if path.isdir(self.__path):
            self.__path = path.join(self.directory, val)
        else:
            self.__path = path.join(self.directory, val, self.extension)
        self.broadcast()


    # extension property
    @property
    def extension(self) -> str:
        if path.isdir(self.__path):
            return None
        return path.splitext(path.basename(self.__path))[1]
    @extension.setter
    def extension(self, val:str):
        if path.isdir(self.__path):
            pass
        self.__path = path.join(self.directory, )
        self.broadcast()
