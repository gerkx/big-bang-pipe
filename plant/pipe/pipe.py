import os, shutil
import os.path as path


from .fso import create_FSO, FSO


class Pipe:
    def __init__(self, 
        dir:str, 
        reject_dir:str,
        queues:object, 
        filters:list, 
        fittings:list, 
        recurse:bool = False,
    ):
        self.directory:str = dir
        self.reject_directory:str = reject_dir
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
        fso_list:list = []
        for obj in self.pipe_contents():
            props = self.filter(obj)
            if props:
                new_fso = self.create_fso(obj, props)
                fso_list.append(new_fso)
        return fso_list

    def check_existing_pipe_contents(self):
        for fso in self._contents:
            if not fso.locked:
                if not path.exists(fso.path) or str(fso.state) == 'FINISHED':
                    self.remove_fso(fso)

    def check_new_pipe_contents(self):
        for obj in self.pipe_contents():
            if obj not in [fso.path for fso in self._contents]:
                props = self.filter(obj)
                if props:
                    new_fso = self.create_fso(obj, props)
                    self._contents.append(new_fso)

    def filter(self, fso_path):
        name:str = path.splitext(path.basename(fso_path))[0]
        if not any([filter.match(name) for filter in self.filters]):
            self.reject(fso_path)
        else:
            filtro = next(filter for filter in self.filters if filter.match(name))
            return filtro.extract_vals(name)


    
    def create_fso(self, fso_path, props):
        new_fso = create_FSO(
            fso_path,
            [fitting(self.queues) for fitting in self._fittings],
            props,
            self.queues.io
        )
        # self._contents.append(new_fso)
        new_fso.subscribe(self.antenna)
        return new_fso
    
    def reject(self, fso_path):
        reject_path = path.join(self.reject_directory, path.basename(fso_path))
        print(f'{fso_path} doesn\'t match any filter criterias!')
        shutil.move(fso_path, reject_path)

    def remove_fso(self, fso):
        self._contents.remove(fso)
        if fso.directory == self.directory:
            shutil.rmtree(fso.path) if path.isdir(fso.path) else os.remove(fso.path)

