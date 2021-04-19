from typing import Callable, Type
from enum import Enum, auto


class State(Enum):
    PENDING = auto()
    QUEUED = auto()
    PROCESSING = auto()
    FINISHED = auto()
    ERROR = auto()


class Fitting_State:
    def __init__(self, callback:Callable):
        self.__state:Type[State] = State.PENDING
        self.callback:Callable = callback
        # self.__idx:int = 0
        # self._stages:list = ['pending', 'queued', 'processing', 'finished', 'error']

    def __repr__(self): 
        return self.__str__()
    
    def __str__(self):
        return self.__state.name

    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, state:Type[State]):
        self.__state = state
        self.broadcast()

    def broadcast(self):
        self.callback()

    def enqueue(self):
        self.state = State.QUEUED

    def process(self):
        self.state = State.PROCESSING

    def finish(self):
        if not self.state == State.ERROR:
            self.state = State.FINISHED
    
    def raise_error(self):
        self.state = State.ERROR
        

