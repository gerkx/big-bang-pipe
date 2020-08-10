# from typing import Callable

class FSO_State:
    def __init__(self, fittings:list, parent_callback):
        self._stages:list = ['pending', 'ready', 'processing', 'finished', 'error']
        self._subscribers:list = [parent_callback,]
        self.__idx:int = 0
        self.__fitting_idx:int = 0
        self.fittings:list = fittings

        self.subscribe_to_fittings()

    def __str__(self):
        # return self.stage()
        return self.summary

    def fitting_state(self) -> str:
        return self.fittings[self.__fitting_idx].state

    @property
    def summary(self) -> str:
        if self.stage() != 'processing':
            return self.stage()
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
        for fitting in self.fittings:
            fitting.subscribe(self.fitting_antenna)

    def subscribe(self, callback):
        self._subscribers.append(callback)

    def broadcast(self):
        for callback in self._subscribers:
            callback()

    def ready(self):
        if self.stage() == 'pending':
            self.set_idx('ready')
        self.broadcast()
        return
    
    def process(self):
        if self.stage() == 'ready':
            self.set_idx('processing')
        
    def finish(self):
        if self.stage() == 'processing':
            self.set_idx('finished')

    def raise_error(self):
        self.set_idx('error')

    def fitting_antenna(self):
        fitting = self.fittings[self.__fitting_idx]
        if fitting.state == 'error':
            self.raise_error()
        if fitting.state == 'finished':
            if self.__fitting_idx == len(self.fittings) - 1:
                print('finished')
                self.finish()
            else:
                self.__fitting_idx += 1
                fitting = self.fittings[self.__fitting_idx]
                fitting.enqueue()
        self.broadcast()
        return
        
