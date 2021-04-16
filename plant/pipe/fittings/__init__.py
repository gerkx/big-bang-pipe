# import pkgutil

# __all__ = []
# for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
#     __all__.append(module_name)
#     _module = loader.find_module(module_name).load_module(module_name)
#     globals()[module_name] = _module


from .audio_grab_fittings import (
    Rename_Audio_Grab, 
    Move_Audio_Grab_To_Server, 
    Copy_Audio_Grab_To_Edit, 
    Save_Audio_Grab_To_DB,
    Add_Audio_To_WorkingAudio_DB,
    Add_MP3_To_DB
)

from .ffmpeg_fittings import (
    Transcode_To_MP3, 
    Transcode_To_MP4,
    Transcode_To_MJPEG_QT,
    Transcode_Char_Audio,
    Transcode_EXR_To_ProRes4444,
)

from .asana_fittings import (
    Asana_Create_Task
)

from .animatic_fittings import (
    Move_Animatic_To_Exchange, 
    Save_Shot_To_DB, 
    Zip_Char_Audios,
    Copy_Shots_To_Edit,
    Add_Shot_To_WorkingPost_DB,
    Remove_Original_QT
)

from .motion_fittings import (
    Move_Motion_To_Server,
    Save_Motion_To_DB,
    Copy_Motion_To_Edit,
    Add_Motion_To_WorkingPost_DB,
    Add_MP4_To_DB,

)

from .compo_fittings import (
    Move_Compo_To_Server,
    Generate_Shot_Name,
    Save_Compo_To_DB,
    Copy_Compo_To_Edit,
    Add_Compo_To_WorkingPost_DB,
)

from .grade_fittings import (
    Move_Grade_To_Server,
    Generate_Shot_Name,
    Save_Grade_To_DB,
    Generate_Edit_Dirs,
    Get_WorkingDB_Shot,
    Update_Edit_Shot,
)

from .render_fittings import *