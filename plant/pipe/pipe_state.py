class Pipe_State:
    def __init__(self, fittings:list):
        self.__idx:int = 0
        self._stages:list = ['pending', 'ready', 'processing', 'finished', 'error']
        self.fittings:list = fittings
        self.__fitting_idx:int = 0

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

    def advance(self):
        if self.__idx < self._stages.index('finished'):
            self.__idx += 1

    def pending(self):
        self.__idx = self._stages.index('pending')

    def ready(self):
        self.__idx = self._stages.index('ready')

    def processing(self):
        self.__idx = self._stages.index('processing')

    # TODO: def update(self):
