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
        static:bool = await file_is_static()
        free = file_is_free()

        if static and free:
            available = True
    
    return True

async def dir_is_static(dir:str) -> bool:
    prelim_hash:str = ""
    for file in walk_dir(dir):
        prelim_hash += hashfile(file)
    await asyncio.sleep(2)
    secondary_hash:str = ""
    for file in walk_dir(dir):
        secondary_hash += hashfile(file)
    
    if prelim_hash == secondary_hash:
        return True
    
    return False
        

if __name__ == "__main__":
    filepath = "Q:\\Dropbox (BigBangBoxSL)\\PROYECTOS\\My preschool monster serie\\PRODUCCION\\Editorial\\Render\\CAT\\S01E04\\momonsters_04_T01_2019_CAT_v001.mov"
    start = time.time()
    h = asyncio.run(file_is_available(filepath))
    # h:str = hashfile(filepath)
    print(time.time()-start)
    print(h)
    # boop = beep(test)

    # boop.yarp.name()

    # boop.name = "zoinks"
    
    # boop.yarp.name()