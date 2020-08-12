from typing import Callable

class Fitting_State:
    def __init__(self, callback:Callable):
        self.callback:Callable = callback
        self.__idx:int = 0
        self._stages:list = ['pending', 'queued', 'processing', 'finished', 'error']

    def __repr__(self): 
        return self.__str__()
    
    def __str__(self):
        return self.stage()

    def stage(self) -> str:
        return self._stages[self.__idx]

    def set_idx(self, key):
        try:
            self.__idx = self._stages.index(key)
        except:
            # TODO: implement error handling
            pass
    
    def broadcast(self):
        self.callback()

    def enqueue(self):
        if self.stage() == 'pending':
            self.set_idx('queued')
            self.broadcast()

    def process(self):
        if self.stage() == 'queued':
            self.set_idx('processing')
            self.broadcast()

    def finish(self):
        if self.stage() == 'processing':
            self.set_idx('finished')
            self.broadcast()
    
    def raise_error(self):
        self.set_idx('error')
        self.broadcast()




