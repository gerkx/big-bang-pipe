import os
import os.path as path

class FSO:
    def __init__(self, path):
        self.name = path

class Pipe:
    def __init__(self, dir:str, queues:dict, template:dict, recurse:bool = False,):
        self.pipe:str = dir
        self.queues:dict = queues
        self.template:dict = template
        self.recurse:bool = recurse
        self.contents:list = self.init_pipe_contents()

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
        return [FSO(obj) for obj in self.pipe_contents()]
