from typing import Type
from enum import Enum, auto


class State(Enum):
    PENDING = auto()
    READY = auto()
    LIMBO = auto()
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
        return self.__state.name

    # observer pattern methods
    def subscribe(self, callback):
        self._subscribers.append(callback)

    def broadcast(self, event):
        for callback in self._subscribers:
            callback(event)

    def antenna(self):
        fitting_state = str(self.fitting.state)
        # handle fitting error
        if fitting_state == 'ERROR':
            self.raise_error()
        
        # handle fitting finish
        if fitting_state == 'FINISHED':
            # all fittings finished
            if self.__fitting_idx == len(self.fittings) - 1:
                self.finish()
                self.broadcast('all done!!!')
            # or advance to the next fitting
            else:
                self.limbo()
                self.broadcast('fitting finished')
                self.advance_fitting()
        
        # handle fitting processing
        if fitting_state == 'PROCESSING':
            self.process()
            self.broadcast('set state to processing')

        # handle fitting enqueue
        if fitting_state == 'QUEUED':
            self.queue()
            self.broadcast('task queued')
    # ####################################################

    # properties an property specific methods
    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, state:Type[State]):
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

    def queue(self):
        self.state = State.QUEUED

    def limbo(self):
        self.state = State.LIMBO

    def raise_error(self):
        self.state = State.ERROR
        
