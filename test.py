from plant.pipe.fso.fso import create_FSO
from plant.queues.async_queue import ASYNC_Queue
        

if __name__ == "__main__":
    import asyncio
    from plant.queues.async_queue import ASYNC_Queue
    queue = ASYNC_Queue()

    # queue = asyncio.Queue()

    filepath = "F:\\tmp\\_seq"
    
    asyncio.get_event_loop().run_until_complete(create_FSO(filepath, queue))
    asyncio.get_event_loop().run_until_complete(create_FSO(filepath + "\\boop.mp4", queue))