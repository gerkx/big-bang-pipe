# from plant.pipe.fso.fso import create_FSO
from plant.pipe import Pipe
from plant.pipe.pipe_utils import init_Pipe
# from plant.pipe.pipe import Pipe
# from plant.queues.fifo_queue import FIFO_Queue
from plant.queues import Queue
from plant.pipe.filters.filter import Filter

import time
from box import Box

if __name__ == "__main__":
    from plant.pipe.fittings.test_fitting import Test_Fitting
    from plant.pipe.fittings.test_fitting2 import Test_Fitting2
    queues = Queue()

    class_str = "Test_Fitting"

    watch = "F:\\tmp\\watch"
    reject = "F:\\tmp\\reject"

        
    print(globals()['Test_Fitting'])

    config = {
        'dir' : watch,
        'reject_dir' : reject,
        'fittings' : ['Test_Fitting'],
        'filters' : ['${prefix}_S${sea}E${epi}_SH${shot}']
    }

    pipes = [init_Pipe(queues, **config)]
    try:
        while True:
            for pipe in pipes:
                pipe.update()
            time.sleep(1)
    except KeyboardInterrupt:
        queues.io.deactivate()
    # print(instance)

    # time.sleep(2)
    # # queues.io.deactivate()
    # print('lllll')

    # time.sleep(2)
    # queues.io.deactivate()
    # print('zzzzzzzzzzzzzzzzzzzzzz')
    # filter_str = '${prefix}_S${sea}E${epi}_SH${shot}'

    # test_name = 'monster_S6E45_SH0035'


    # fittings = [Test_Fitting]

    # fltr = Filter(filter_str)

    # pipa = Pipe(watch, reject, queues, [fltr], fittings)

    # while True:
    #         pipa.update()
    #         time.sleep(1)

    # try:
    #     while True:
    #         pipa.update()
    #         time.sleep(1)

    # except KeyboardInterrupt:
    #     queues.io.deactivate()
    

    




    # data = [
    #     [11.4, 3.56, 0.62],
    #     [11.2, 4.75, 1.00],
    #     [10.8, 5.40, 1.05],
    #     [11.2, 5.20, 2.08],
    #     [11.2, 3.99, 1.55],
    #     [11.4, 4.10, 4.15],
    #     [12.5, 3.79, 3.99],
    #     [10.0, 2.28, 3.46],
    #     [11.8, 2.25, 4.20],
    #     [9.8, 1.30, 2.0],
    #     [9.5, 0.75, 1.07],
    #     [9.0, 1.35, 1.63],
    #     [8.9, .89, 0.17],
    #     [10.4, 1.20, 1.30],
    #     [11.0, 1.90, 2.10],
    #     [11.0, 2.13, 2.20],
    #     [10.2, 1.00, 2.00],
    #     [9.5, 0.50, 0.50],
    #     [9.5, 1.50, 1.20],
    #     [9.8, 1.80, 2.00],
    #     [11.0, 2.60, 3.40],
    #     [11.4, 3.50, 3.50],
    #     [12.3, 3.80, 3.20],
    #     [12.0, 2.80, 2.70],
    #     [11.7, 2.10, 2.70],
    #     [11.2, 4.50, 1.00],
    #     [11.3, 4.30, 1.00],
    #     [11.4, 3.20, 2.50],
    # ]
    # hghts = [arr[0] for arr in data]

    # def avg(arr):
    #     acc = 0
    #     for h in arr:
    #         acc += h

    #     avg = acc / len(arr)
    #     return avg
    
    # order = sorted(hghts)

    # import statistics

    # print(statistics.mean(hghts))
    # print(statistics.median(hghts))


    # print(order)
    # last = len(hghts)-2
    # print(order[2:last])
    # no_outlier = order[2:last]
    # print(avg(hghts))
    # print(avg(no_outlier))
    # print(avg(hghts))
