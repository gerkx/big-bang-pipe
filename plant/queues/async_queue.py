import asyncio, time

class ASYNC_Queue: 
    def __init__(self, loop):
        # self.sync:bool = False
        self.loop = loop
        self.queue = asyncio.Queue()
        # self.tasks: list = []

    async def async_worker(self):
        while not self.queue.empty():
        # while True:
            task = await self.queue.get()
            await task()
            # obj, task = await self.queue.get()
            # await getattr(obj, task)()
            self.queue.task_done()

    async def add(self, *tasks: object):
        print (f'adding {tasks[0]}')
        tasklist: list = []
        for task in tasks:
            self.queue.put_nowait(task)
            tasklist.append(asyncio.create_task(self.async_worker()))
            self.loop.run_until_complete(tasklist)
        # asyncio.run(asyncio.gather(*tasklist))
        # try:
        #     loop = asyncio.get_running_loop()
        # except RuntimeError:
        #     loop = None

        # if loop and loop.is_running():
        # else:
        #     asyncio.run(tasklist)

    