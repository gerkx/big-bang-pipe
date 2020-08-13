from typing import Type
from enum import Enum, auto

class State(Enum):
    PENDING = auto()
    READY = auto()
    QUEUED = auto()
    PROCESSING = auto()
    FINISHED = auto()
    ERROR = auto()

class FSO_State:
    def __init__(self, fittings:list, parent:object):
        self.__state:Type[State] = State.PENDING
        self._subscribers:list = [parent.antenna,]
        self.__idx:int = 0
        self.__fitting_idx:int = 0
        self.fittings:list = self.setup_fittings(fittings, parent)

    
    def __str__(self):
        return self.state.name

    # observer pattern methods
    def subscribe(self, callback):
        self._subscribers.append(callback)

    def broadcast(self, event):
        for callback in self._subscribers:
            callback(event)

    def antenna(self):
        # handle fitting error
        if self.fitting.state.stage() == 'error':
            self.raise_error()
        
        # handle fitting finish
        if self.fitting.state.stage() == 'finished':
            # all fittings finished
            if self.__fitting_idx == len(self.fittings) - 1:
                self.finish()
                self.broadcast('all done!!!')
            # or advance to the next fitting
            else:
                self.advance_fitting()
                self.broadcast('queued next fitting')
        
        # handle fitting processing
        if self.fitting.state.stage() == 'processing':
            self.process()
            self.broadcast('set state to processing')

        # handle fitting enqueue
        if self.fitting.state.stage() == 'queued':
            self.state = State.QUEUED
            self.broadcast('task queued')
    # ####################################################

    # properties an property specific methods
    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, state):
        self.__state = state

    @property
    def fitting(self):
        return self.fittings[self.__fitting_idx]
    
    def advance_fitting(self):
        self.__fitting_idx += 1
        self.fitting.enqueue()

    def fitting_state(self) -> str:
        return self.fittings[self.__fitting_idx].state
      
    def setup_fittings(self, fittings, parent):
        init_fittings:list = []
        for fitting in fittings:
            fitting.subscribe(self.antenna)
            fitting.set_parent(parent)
            init_fittings.append(fitting)
        return init_fittings

    @property
    def summary(self) -> str:
        if self.state != State.PROCESSING:
            return self.state.name
        else:
            total = len(self.fittings)
            current = self.__fitting_idx + 1
            status = self.fitting_state()
            return f'processing: task {current} of {total} is {status}'
    # ######################################################

    # state methods
    def ready(self):
        self.state = State.READY
        self.broadcast('all ready')
        self.fitting.enqueue()
    
    def process(self):
        self.state = State.PROCESSING
        
    def finish(self):
        self.state = State.FINISHED

    def raise_error(self):
        self.state = State.ERROR
        
