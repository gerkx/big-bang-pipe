import asyncio, time

class ASYNC_Queue: 
    def __init__(self):
        self.sync:bool = False
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        # self.tasks: list = []

    async def async_worker(self):
        while not self.queue.empty():
        # while True:
            task = await self.queue.get()
            task()
            # obj, task = await self.queue.get()
            # await getattr(obj, task)()
            self.queue.task_done()

    async def add(self, *tasks: object):
        print (f'adding {tasks[0]}')
        tasklist: list = []
        for task in tasks:
            self.queue.put_nowait(task)
            tasklist.append(self.loop.create_task(await self.async_worker()))
        self.loop.run_until_complete(asyncio.gather(*tasklist))

    

    