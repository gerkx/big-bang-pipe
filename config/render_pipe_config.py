from .dirs import RENDER_INBOX, REJECT_INBOX, ROOT_DIR, SERVER_DIR

from plant.templates import render_template

render_pipe_config = {
    'name': 'render_pipe',
    'dir': RENDER_INBOX,
    'reject_dir': REJECT_INBOX,
    'filters': [render_template],
    'fittings': {
        'render': [
            'Set_Prod_Number',
            'Generate_Shot_Name',
            'Get_Project_DB', 'Get_Shot_DB',
            'Get_Version_Number', 
            'Rename_Dir_With_Vers', 
            'Extract_All_Dirs', 
            'Detect_IMG_Sequences',
            'Check_For_Seq_Gaps',
            'Rename_Seq_With_Vers',
            'Move_Render_To_Server', 
            'Generate_Transcode_Dirs',
            'Transcode_EXR_To_ProRes4444', 
            'Save_Render_To_DB',
            'Render_Generate_Edit_Dirs', 
            'Transcode_To_MP4',
            'Render_Get_WorkingDB_Shot', 
            'Establish_Working_Dir',
            'Update_Working_Shot', 
            'Update_WorkingDB',
            'Asana_Create_Task',
            'Update_Excel',
        ]
    },
    'props': {
        'client': 'monster',
        'editorial': ROOT_DIR,
        'server': SERVER_DIR,
        'program': 'monster'
    }
}