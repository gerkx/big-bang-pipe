import os
import os.path as path

from .fso import create_FSO


class Pipe:
    def __init__(self, dir:str, queues:dict, template:dict, fittings:list, recurse:bool = False,):
        self.pipe:str = dir
        self.queues:dict = queues
        self.template:dict = template
        self.recurse:bool = recurse
        self._contents:list = self.init_pipe_contents()
        self._fittings:list = fittings

    def poll(self):
        pass

    def pipe_contents(self) -> list:
        if not self.recurse:
            return [path.join(self.pipe, item) for item in os.listdir(self.pipe)]
        else:
            dir:list = []
            for root, _, files in os.walk(self.pipe):
                for f in files:
                    dir.append(path.join(root, f))
            return dir

    # TODO: figure a way to init each fitting with the appropriate queue... 
    # maybe just pass the dict and have that be a constant api for the fittings... **kwargs 
    def init_pipe_contents(self) -> list:
        return [create_FSO(obj, self._fittings, self.queues['fifo']) for obj in self.pipe_contents()]

    def check_existing_pipe_contents(self):
        for fso in self._contents:
            if not path.exists(fso.path):
                print(f'fso {fso.name} not found, deleting instance and removing from list')
                self._fittings.remove(fso)
                del fso

    def check_new_pipe_contents(self):
        for obj in self.pipe_contents():
            if obj not in [fso.path for fso in self._contents]:
                self._contents.append(
                    create_FSO(obj, self._fittings, self.queues['fifo'])
                )

