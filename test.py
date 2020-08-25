# from plant.pipe.fso.fso import create_FSO
from plant.pipe import Pipe
from plant.pipe.pipe_utils import init_Pipe
# from plant.pipe.pipe import Pipe
# from plant.queues.fifo_queue import FIFO_Queue
from plant.queues import Queue
from plant.pipe.filters.filter import Filter


from plant import Plant

import time
from box import Box

import httpx
import json
import asyncio
if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    queues = Queue()
    json_url = 'https://jsonplaceholder.typicode.com/posts'

    
    # from plant.pipe.fittings.test_fitting import Test_Fitting
    # from plant.pipe.fittings.test_fitting2 import Test_Fitting2
    from plant.pipe.fittings.base_fittings.async_fitting import Async_Fitting

    class_str = "Async_Fitting"
    watch = "F:\\tmp\\watch"
    reject = "F:\\tmp\\reject"

    filtro = {
        'template': '${prefix}_S${sea}E${epi}_SQ${seq}_SH${shot}_INT${frame}',
        'definitions': {
            'prefix': {
                'type': 'alpha_numeric',
                'options': {
                    "min_length": 1
                }
            },
            'sea': {
                'type': 'numeric',
                'options': {
                    "min_length": 1,
                    "max_length": 5
                }
            },
            'epi': {
                'type': 'numeric',
                'options': {
                    "min_length": 1,
                    "max_length": 5
                }
            },
            'seq': {
                'type': 'numeric',
                'options': {
                    "min_length": 1,
                    "max_length": 5
                }
            },
            'shot': {
                'type': 'numeric',
                'options': {
                    "min_length": 1,
                    "max_length": 5
                }
            },
            'frame': {
                'type': 'numeric',
                'options': {
                    "min_length": 1,
                    "max_length": 5
                }
            },
        }
    }
    
    config = [{
        'name': 'test_pipe',
        'dir' : watch,
        'reject_dir' : reject,
        'fittings' : [class_str],
        'filters' : [filtro],
        'props': {'base_dir': "F:\\tmp\\dos"}
    }]

    
    plant = Plant(queues, config)

    plant.start()
    







    




    # # pipes = [init_Pipe(queues, **config)]
    # # try:
    # #     while True:
    # #         for pipe in pipes:
    # #             pipe.update()
    # #         time.sleep(1)
    # # except KeyboardInterrupt:
    # #     queues.io.deactivate()




    # # data = [
    # #     [11.4, 3.56, 0.62],
    # #     [11.2, 4.75, 1.00],
    # #     [10.8, 5.40, 1.05],
    # #     [11.2, 5.20, 2.08],
    # #     [11.2, 3.99, 1.55],
    # #     [11.4, 4.10, 4.15],
    # #     [12.5, 3.79, 3.99],
    # #     [10.0, 2.28, 3.46],
    # #     [11.8, 2.25, 4.20],
    # #     [9.8, 1.30, 2.0],
    # #     [9.5, 0.75, 1.07],
    # #     [9.0, 1.35, 1.63],
    # #     [8.9, .89, 0.17],
    # #     [10.4, 1.20, 1.30],
    # #     [11.0, 1.90, 2.10],
    # #     [11.0, 2.13, 2.20],
    # #     [10.2, 1.00, 2.00],
    # #     [9.5, 0.50, 0.50],
    # #     [9.5, 1.50, 1.20],
    # #     [9.8, 1.80, 2.00],
    # #     [11.0, 2.60, 3.40],
    # #     [11.4, 3.50, 3.50],
    # #     [12.3, 3.80, 3.20],
    # #     [12.0, 2.80, 2.70],
    # #     [11.7, 2.10, 2.70],
    # #     [11.2, 4.50, 1.00],
    # #     [11.3, 4.30, 1.00],
    # #     [11.4, 3.20, 2.50],
    # # ]
    # # hghts = [arr[0] for arr in data]

    # # def avg(arr):
    # #     acc = 0
    # #     for h in arr:
    # #         acc += h

    # #     avg = acc / len(arr)
    # #     return avg
    
    # # order = sorted(hghts)

    # # import statistics

    # # print(statistics.mean(hghts))
    # # print(statistics.median(hghts))


    # # print(order)
    # # last = len(hghts)-2
    # # print(order[2:last])
    # # no_outlier = order[2:last]
    # # print(avg(hghts))
    # # print(avg(no_outlier))
    # # print(avg(hghts))
