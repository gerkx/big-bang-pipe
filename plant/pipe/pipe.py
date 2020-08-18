import os
import os.path as path

import gc
# from threading import Thread

from .fso import create_FSO, FSO


class Pipe:
    def __init__(self, dir:str, queues:object, template:dict, fittings:list, recurse:bool = False,):
        self.pipe:str = dir
        self.queues:object = queues
        self.template:dict = template
        self.recurse:bool = recurse
        self._fittings:list = fittings
        self._contents:list = self.init_pipe_contents()
        self.__active:bool = True

    @property
    def active(self):
        return self.__active

    def activate(self):
        if not self.__active:
            self.__active = True

    def deactivate(self):
        if not self.__active:
            self.__active = False

    def update(self):
        if self.active:
            self.check_existing_pipe_contents()
            self.check_new_pipe_contents()

    def antenna(self, guid):
        fso = next(obj for obj in self._contents if obj.guid == guid)
        print('-+'*10)
        print(f'pipe says that {fso.name} is {fso.state}')
        print('-+'*10)


    def pipe_contents(self) -> list:
        if not self.recurse:
            return [path.join(self.pipe, item) for item in os.listdir(self.pipe)]
        else:
            dir:list = []
            for root, _, files in os.walk(self.pipe):
                for f in files:
                    dir.append(path.join(root, f))
            return dir

    
    def init_pipe_contents(self) -> list:
        fso_list = [
            create_FSO(
                obj, 
                [fitting(self.queues) for fitting in self._fittings], 
                self.queues.fifo) 
                for obj in self.pipe_contents()
        ]
        [fso.subscribe(self.antenna) for fso in fso_list]
        return fso_list

    def check_existing_pipe_contents(self):
        # rmv_q = []
        for fso in self._contents:
            print(f'checking that {fso.name} still exists')
            if not path.exists(fso.path):
                print(f'fso {fso.name} not found, deleting instance and removing from list -- {fso}')
                self._contents.remove(fso)

    def check_new_pipe_contents(self):
        print('checking for new pipe contents')
        for obj in self.pipe_contents():
            if obj not in [fso.path for fso in self._contents]:
                print(f'{obj} appears to be new! initializing fso')
                new_fso = create_FSO(
                    obj, 
                    [fitting(self.queues) for fitting in self._fittings], 
                    self.queues.fifo
                )
                self._contents.append(new_fso)
                new_fso.subscribe(self.antenna)

    def reject(self):
        pass

