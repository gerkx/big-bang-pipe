import time
import asyncio, os
from os import path
from imohash import hashfile

def walk_dir(dir:str) -> list:
    dir_files: list = []
    for root, _, files in os.walk(dir):
        for f in files:
            dir_files.append(path.join(root, f))
    return dir_files

async def file_is_available(filepath:str) -> bool:
    
    def file_is_free() -> bool:
        test_path:str = path.join(path.dirname(filepath), f'_{path.basename(filepath)}')
        try:
            os.rename(filepath, test_path)
            os.rename(test_path, filepath)
            return True
        except OSError:
            pass

        return False

    async def file_is_static() -> bool:
        prelim_hash:str = hashfile(filepath)
        await asyncio.sleep(1)
        secondary_hash:str = hashfile(filepath)

        if prelim_hash == secondary_hash:
            return True
        
        return False


    available:bool = False
    while not available:
        free:bool = file_is_free()
        if free:
            static:bool = await file_is_static()

        free = file_is_free()
        if static and free:
            available = True
    
    return True

async def dir_is_static(dir:str, interval:int=2) -> bool:
    available:bool = False
    while not available:
        try:
            print('hash #1')
            prelim_hash:list = [hashfile(file) for file in walk_dir(dir)]
            print('sleep')
            await asyncio.sleep(interval)
            print('awake')
            print('hash #2')
            secondary_hash:list = [hashfile(file) for file in walk_dir(dir)]
        
            if prelim_hash == secondary_hash:
                available = True
        except:
            print('file in use')
            available = False
    
    return True

async def dir_is_available(dir:str):
    def file_is_free(f) -> bool:
        test_path:str = path.join(path.dirname(f), f'_{path.basename(f)}')
        try:
            os.rename(f, test_path)
            os.rename(test_path, f)
            return True
        except OSError:
            pass

        return False

    available:bool = False
    while not available:
        static:bool = False
        free:bool = False
        # print(beep)
        
        barp = [file_is_free(file) for file in walk_dir(dir)]
        print(barp)
        print(False in barp)
        available=True
        #     print(file)
            # free = file_is_free(file)
            # print(f'checking if free: {free}')
        # if free:
            # static:bool = await dir_is_available(dir)
        print('yikes')
        # for file in walk_dir(directory):
        #     free = file_is_free(file)
        if static and free:
            available = True
    
    return True
        

if __name__ == "__main__":
    # filepath = "Q:\\Dropbox (BigBangBoxSL)\\PROYECTOS\\My preschool monster serie\\PRODUCCION\\Editorial\\Render\\CAT\\S01E04\\momonsters_04_T01_2019_CAT_v001.mov"
    filepath = "F:\\tmp\\_seq"
    path2 = "F:\\tmp\\out"
    start = time.time()
    h = asyncio.run(dir_is_static(filepath))
    h = asyncio.run(dir_is_static(path2))
    # h:str = hashfile(filepath)
    print(time.time()-start)
    print(h)
    # boop = beep(test)

    # boop.yarp.name()

    # boop.name = "zoinks"
    
    # boop.yarp.name()