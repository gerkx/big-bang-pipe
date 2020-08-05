class Fitting_State:
    def __init__(self):
        self.__idx:int = 0
        self._stages:list = ['pending', 'queued' 'processing', 'finished', 'error']

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return self._stages[self.__idx]

    def activate(self):
        if self.__idx == 0:
            self.__idx = 1

    def finish(self):
        if self.__idx == 1:
            self.idx = 2
    
    def raise_error(self):
        self.__idx = self._stages.index('error')

    @property
    def state(self) -> str:
        return self._stages[self.__idx]


