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

    # from peewee import *
    from datetime import date
    from nanoid import generate

    from peewee import OperationalError

    from plant.database.models import (
        Client, Project, Shot, AudioGrab, Music, Mix, Stem, WorkingAudio, 
        Asana_Project, Asana_Tag, Asana_Task, Asana_User
    )


    try:
        Client.create_table()
    except OperationalError:
        print('Client table already exists')
    try:
        Project.create_table()
    except OperationalError:
        print('Project table already exists')
    try:
        Shot.create_table()
    except OperationalError:
        print('Shot table already exists')
    try:
        AudioGrab.create_table()
    except OperationalError:
        print('AudioGrab table already exists')
    try:
        Music.create_table()
    except OperationalError:
        print('Music table already exists')
    try:
        Mix.create_table()
    except OperationalError:
        print('Mix table already exists')
    try:
        Stem.create_table()
    except OperationalError:
        print('Stem table already exists')
    try:
        WorkingAudio.create_table()
    except OperationalError:
        print('WorkingAudio table already exists')
    try:
        Asana_User.create_table()
    except OperationalError:
        print('Asana_User table already exists')
    try:
        Asana_Task.create_table()
    except OperationalError:
        print('Asana_Task table already exists')
    try:
        Asana_Project.create_table()
    except OperationalError:
        print('Asana_Project table already exists')
    try:
        Asana_Tag.create_table()
    except OperationalError:
        print('Asana_Tag table already exists')


    gerkx = Client().new_or_get('gerkx')


    from plant.templates.audio.audio_grab import audio_grab_template


    fittings = [
        'Rename_Audio_Grab', 'Move_Audio_Grab_To_Server', 'Save_Audio_Grab_To_DB',
        'Copy_Audio_Grab_To_Edit', 'Add_Audio_To_WorkingAudio_DB', 'Asana_Create_Task',
        # 'Transcode_To_MP3', 'Add_MP3_To_DB'
    ]

    watch = "F:\\tmp\\watch"
    reject = "F:\\tmp\\reject"
    edit = "F:\\tmp\\edit"
    server = 'F:\\tmp\\server'

    
    config = [{
        'name': 'audio_grab',
        'dir' : watch,
        'reject_dir' : reject,
        'fittings' : fittings,
        'filters' : [audio_grab_template],
        'props': {'client': 'monster', 'editorial': edit, 'season': 2, 'server': server, 'program': 'monster' }
    }]

    
    plant = Plant(config)

    # plant.start()
    







    




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
