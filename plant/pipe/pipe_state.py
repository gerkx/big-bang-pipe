from typing import Callable

class Pipe_State:
    def __init__(self, fittings:list):
        self.__idx:int = 0
        self._stages:list = ['pending', 'ready', 'processing', 'finished', 'error']
        self.fittings:list = fittings
        self.__fitting_idx:int = 0
        self._subscribers:list = []

        self.subscribe_to_fittings()

    def __str__(self):
        return self.summary()

    def fitting_state(self) -> str:
        return self.fittings[self.__fitting_idx].state

    @property
    def summary(self) -> str:
        if self.__idx != self._stages.index('processing'):
            return self._stages[self.__idx]
        else:
            total = len(self.fittings)
            current = self.__fitting_idx + 1
            status = self.fitting_state()
            return f'processing: task {current} of {total} is {status}'
    
    def stage(self) -> str:
        return self._stages[self.__idx]

    def set_idx(self, key):
        try:
            self.__idx = self._stages.index(key)
        except:
            # TODO: implement error handling
            pass
        
    def subscribe_to_fittings(self):
        for idx, fitting in enumerate(self.fittings):
            fitting.subscribe(idx, self.fitting_update)

    def subscribe(self, idx:int, callback:Callable[[int, str]]):
        self._subscribers.append({
            'idx': idx,
            'callback': callback
        })

    def broadcast(self):
        for sub in self._subscribers:
            idx = sub['idx']
            callback = sub['callback']
            callback(idx, self.summary)

    def ready(self):
        if self.stage() == 'pending':
            self.set_idx('ready')
    
    def process(self):
        if self.stage() == 'ready':
            self.set_idx('processing')
        
    def finish(self):
        if self.stage() == 'processing':
            self.set_idx('finished')

    def raise_error(self):
        self.set_idx('error')

    def fitting_update(self, fitting_idx:int, fitting_state:str):
        if fitting_state == 'error':
            self.set_idx('error')
        elif self.fitting_state == 'finished':
            if self.__fitting_idx == len(self.fittings) - 1:
                self.set_idx('finished')
            else:
                self.__fitting_idx += 1
                # pick up here
                # figure out enqueing!!!!
        else:
            pass
            
        
