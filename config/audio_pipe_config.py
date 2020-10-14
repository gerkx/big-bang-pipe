from .dirs import AUDIO_INBOX, REJECT_INBOX, ROOT_DIR

from plant.templates import audio_grab_template

audio_pipe_config = {
    'name': 'audio_pipe',
    'dir': AUDIO_INBOX,
    'reject_dir': REJECT_INBOX,
    'filters': [audio_grab_template,],
    'fittings': {
        'audio_grab': [
            'Rename_Audio_Grab', 'Move_Audio_Grab_To_Server', 'Save_Audio_Grab_To_DB',
            'Copy_Audio_Grab_To_Edit', 'Add_Audio_To_WorkingAudio_DB', 'Asana_Create_Task',
            'Transcode_To_MP3', 'Add_MP3_To_DB'
        ],
    },
    'props': {
        'client': 'monster',
        'editorial': ROOT_DIR,
        'season': 2,
        'server': 'Z:\\tmpServer',
        'program': 'monster'
    }
}