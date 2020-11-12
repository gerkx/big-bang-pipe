from .dirs import POST_INBOX, REJECT_INBOX, ROOT_DIR, SERVER_DIR

from plant.templates import (
    compo_template,
    grade_template,
    motion_template,
)

post_pipe_config = {
    'name': 'post_pipe',
    'dir': POST_INBOX,
    'reject_dir': REJECT_INBOX,
    'filters': [motion_template, compo_template, grade_template],
    'fittings': {
        'motion': [
            'Move_Motion_To_Server', 'Save_Motion_To_DB',
            'Copy_Motion_To_Edit', 'Add_Motion_To_WorkingPost_DB',
            'Asana_Create_Task', 'Transcode_To_MP4', 'Add_MP4_To_DB'
        ],
        'compo': [
            'Move_Compo_To_Server', 
            'Generate_Shot_Name',
            'Save_Compo_To_DB',
            'Copy_Compo_To_Edit', 'Add_Compo_To_WorkingPost_DB',
            'Asana_Create_Task',
        ],
        'grade': [
            'Move_Grade_To_Server', 
            'Generate_Shot_Name',
            'Save_Grade_To_DB',
            'Generate_Edit_Dirs', 'Get_WorkingDB_Shot',
            'Update_Edit_Shot', 'Asana_Create_Task',
        ]
    },
    'props': {
        'client': 'monster',
        'editorial': ROOT_DIR,
        'server': SERVER_DIR,
        'program': 'monster'
    }
}