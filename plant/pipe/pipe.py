import os, shutil
import os.path as path

import gc
# from threading import Thread

from .fso import create_FSO, FSO


class Pipe:
    def __init__(self, dir:str, queues:object, filters:list, fittings:list, recurse:bool = False,):
        self.directory:str = dir
        self.queues:object = queues
        self.filters:list = filters
        self.recurse:bool = recurse
        self._fittings:list = fittings
        self._contents:list = self.init_pipe_contents()
        self.__active:bool = True
        self.__lock:bool = False

    @property
    def active(self) -> bool:
        return self.__active

    def activate(self):
        if not self.__active:
            self.__active = True

    def deactivate(self):
        if not self.__active:
            self.__active = False

    def update(self):
        print("...")
        if self.active and not self.__lock:
            self.check_existing_pipe_contents()
            self.check_new_pipe_contents()

    def antenna(self, guid):
        self.__lock = True
        fso = next(obj for obj in self._contents if obj.guid == guid)
        fso_state = str(fso.state)
        print('-+'*10)
        print(f'pipe says that {fso.name} is {fso.state.summary}')
        print('-+'*10)
        if fso_state == 'FINISHED':
            self.remove_fso(fso)
        self.__lock = False


    def pipe_contents(self) -> list:
        if not self.recurse:
            return [path.join(self.directory, item) for item in os.listdir(self.directory)]
        else:
            dir:list = []
            for root, _, files in os.walk(self.directory):
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
            if not path.exists(fso.path):
                self._contents.remove(fso)
                
            if str(fso.state) == 'FINISHED':
                self.remove_fso(fso)

    def check_new_pipe_contents(self):
        for obj in self.pipe_contents():
            if obj not in [fso.path for fso in self._contents]:
                new_fso = create_FSO(
                    obj, 
                    [fitting(self.queues) for fitting in self._fittings], 
                    self.queues.fifo
                )
                self._contents.append(new_fso)
                new_fso.subscribe(self.antenna)

    def reject(self):
        pass

    def remove_fso(self, fso):
        # print('zeeeeoooooo')
        self._contents.remove(fso)
        if fso.directory == self.directory:
            shutil.rmtree(fso.path) if path.isdir(fso.path) else os.remove(fso.path)

