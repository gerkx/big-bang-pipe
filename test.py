# from plant.pipe.fso.fso import create_FSO
from plant.pipe.fso import create_FSO

if __name__ == "__main__":
    import asyncio
    # from plant.queues.async_queue import ASYNC_Queue
    from plant.queues.fifo_queue import FIFO_Queue
    queue = FIFO_Queue()


    filepath = "F:\\tmp\\_seq"
    boop = "F:\\tmp\\_seq\\boop.mp4"

    beep = create_FSO(filepath,queue)
    zoop = create_FSO(boop,queue)
    yarp = create_FSO(boop,queue)

    print(f'{beep.name}\'s state is {beep.state}')
    print(f'{zoop.name}\'s state is {zoop.state}')
    print(f'{yarp.name}\'s state is {yarp.state}')