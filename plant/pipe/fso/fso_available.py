import asyncio, os
from os import path
from typing import Callable
from imohash import hashfile

def walk_dir(fso_path:str) -> list:
    dir_files: list = []
    for root, _, files in os.walk(fso_path):
            for f in files:
                dir_files.append(path.join(root, f))
    return dir_files

async def file_is_available(fso_path:str, interval:int=1) -> bool:
    try:
        prelim_hash:str = hashfile(fso_path)
        await asyncio.sleep(interval)
        secondary_hash:str = hashfile(fso_path)

        if prelim_hash == secondary_hash:
            return True
    except:
        pass

    return False

async def dir_is_available(fso_path:str, interval:int=5) -> bool:
    try:
        prelim_hash:list = [hashfile(file) for file in walk_dir(fso_path)]
        await asyncio.sleep(interval)
        secondary_hash:list = [hashfile(file) for file in walk_dir(fso_path)]
    
        if prelim_hash == secondary_hash:
            return True
    except:
        pass

    return False

async def fso_is_available(fso_path:str, callback:Callable):
    print('checking avail')
    available:bool = False
    while not available:
        if path.isdir(fso_path):
            available = await dir_is_available(fso_path)
        else:
            available = await file_is_available(fso_path)
    
    callback()
    return
