from .fitting_state import Fitting_State

class Fitting:
    def __init__(self, queue:object, fso:object):
        self.state:object = Fitting_State()
        self.queue:object = queue
        self.fso:object = fso
        self.task:dict = {
            'obj': self,
            'method': self.main,
            'args': []
        }

    def enqueue_sync(self, task:dict):
        self.queue.add(task)
        self.state.enqueue()

    async def enqueue_async(self, task:dict):
        await self.queue.add(task)
        self.state.enqueue()

    async def enqueue(self, task:dict):
        if self.queue.sync:
            self.enqueue_sync(task)
        else:
            await self.enqueue_async(task)

    def main(self):
        pass