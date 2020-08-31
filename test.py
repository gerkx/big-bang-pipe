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

    # from database.models.client_model import Client
    # from database.models.project_model import Project
    # from database.models.shot_model import Shot
    # from database.models.render_seq_model import RenderSeq

    test_dict = {'name': 'Pat'}

    test_box = Box(test_dict)

    print('name' in test_box)
    print('boop' in test_box)

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
        RenderSeq.create_table()
    except OperationalError:
        print('RenderSeq table already exists')

    # Client().new(name="gerkx")
    # Client().new(name="gerkx")


    gerkx = Client().new_or_get('gerkx')


    workbench = Project().new_or_get(client=gerkx, name='workbench')
    attic = Project().new_or_get(client=gerkx, name='attic')
    kitchen = Project().new_or_get(client=gerkx, name='kitchen')

    top = Shot().new_or_get(project=workbench, name='top', shot='101')
    left = Shot().new_or_get(project=workbench, name='left', shot='102')
    counter = Shot().new_or_get(project=kitchen, name='counter', shot='101')
 
    ver01 = RenderSeq().new_or_get(shot=top, name='top_v001', inbound_name='top', location='attic')
    ver02 = RenderSeq().new_or_get(shot=top, name='top_v002', inbound_name='top', location='attic')

    query = Project.get(Project.name == 'workbench')
    shot = next(shot for shot in query.shots if shot.name == 'top')
    print(len(shot.renders))

    # shots = [shots for shots in query.shots]
    # print(shots[0].name)
    # print(shots[0].renders)
    # vers = [vers for vers in shots.renders]
    # print([ver.name for ver in vers])

    # query = (RenderSeq
    #         .select(RenderSeq, Shot)

    # )


    # print(query.name, query.guid)
    # Project.get_or_create(client = gerkx, name = 'attic', defaults={'guid': generate()})

    # Project.get_or_create(client = gerkx, name = 'workbench', defaults={'guid': generate()})

    # for project in gerkx.projects:
    #     print("xxxxxxx ", project.name, project.guid)
    

    # db = SqliteDatabase('boop.db')

    # class Person(Model):
    #     name = CharField()
    #     birthday = DateField()

    #     class Meta:
    #         database = db

    # class Pet(Model):
    #     owner = ForeignKeyField(Person, backref='pets')
    #     name = CharField()
    #     animal_type = CharField()

    #     class Meta:
    #         database = db

    # db.connect()

    # db.create_tables([Person, Pet])

    # tia_cole = Person(name='Nicole', birthday=date(1985, 5, 3))
    # tia_cole.save()

    # amanda = Person.create(name='Amanda', birthday=date(1982,7,27))

    # tia_cole.name = 'Nikki'
    # tia_cole.save()

    # amanda_cat = Pet.create(owner=amanda, name='Belle', animal_type='cat')
    # nikki_dog = Pet.create(owner=tia_cole, name='Chloe', animal_type='dog')

    # wifey = Person.select().where(Person.name == 'Amanda')

    # sistra = Person.get(Person.name == 'Nikki')

    # query = (
    #     Pet.select(Pet, Person)
    #     .join(Person)
    #     .where(Pet.animal_type == 'cat')
    # )
    
    # for pet in query:
    #     print(pet.name, pet.owner.name)



    # db.close()





    # loop = asyncio.get_event_loop()
    # queues = Queue()
    json_url = 'https://jsonplaceholder.typicode.com/posts'

    
    # from plant.pipe.fittings.test_fitting import Test_Fitting
    # from plant.pipe.fittings.test_fitting2 import Test_Fitting2
    from plant.pipe.fittings.base_fittings.async_fitting import Async_Fitting
    from plant.pipe.fittings.async_test_fitting import Async_Test_Fitting


    class_str = "Async_Test_Fitting"
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
        'props': {'base_dir': "F:\\tmp\\dos", 'url': json_url}
    }]

    
    # plant = Plant(config)

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
