import asyncio
import time

class ASYNC_Queue: 
    def __init__(self):
        self.sync:bool = False
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.tasks: list = []

    async def async_worker(self):
        # while not self.queue.empty():
        while True:
            task = await self.queue.get()
            await task()
            self.queue.task_done()

    async def add(self, *tasks: object):
        tasklist: list = []
        for task in tasks:
            self.queue.put_nowait(task)
            tasklist.append(self.loop.create_task(self.async_worker()))
        self.loop.run_until_complete(asyncio.gather(*tasklist))

    

    