import os, time
from os import path
from typing import Callable
from imohash import hashfile

def walk_dir(fso_path:str) -> list:
    dir_files: list = []
    for root, _, files in os.walk(fso_path):
            for f in files:
                dir_files.append(path.join(root, f))
    return dir_files

def file_is_available(fso_path:str, interval:int=1) -> bool:
    try:
        prelim_hash:str = hashfile(fso_path)
        time.sleep(interval)
        secondary_hash:str = hashfile(fso_path)

        if prelim_hash == secondary_hash:
            return True
    except:
        pass

    return False

def dir_is_available(fso_path:str, interval:int=5) -> bool:
    try:
        prelim_hash:list = [hashfile(file) for file in walk_dir(fso_path)]
        time.sleep(interval)
        secondary_hash:list = [hashfile(file) for file in walk_dir(fso_path)]
    
        if prelim_hash == secondary_hash:
            return True
    except:
        pass

    return False

def check_fso_availability(fso_path:str, callback:Callable):
    print(f'checking avail of {path.basename(fso_path)}')
    available:bool = False
    while not available:
        if path.isdir(fso_path):
            available = dir_is_available(fso_path)
        else:
            available = file_is_available(fso_path)
    
    print(f'{path.basename(fso_path)} is available')
    callback()
    
