from .dirs import REJECT_INBOX, ROOT_DIR, SERVER_DIR, ANIMATIC_EXCHANGE, ANIMATIC_INBOX

from plant.templates import animatic_template

animatic_pipe_config = {
    'name': 'animatic_pipe',
    'dir': ANIMATIC_INBOX,
    'reject_dir': REJECT_INBOX,
    'filters': [animatic_template,],
    'fittings': {
        'animatic': [
            'Move_Animatic_To_Exchange', 
            'Save_Shot_To_DB',
            'Transcode_To_MJPEG_QT', 'Transcode_Char_Audio',
            # 'Zip_Char_Audios', 
            'Copy_Shots_To_Edit',
            'Add_Shot_To_WorkingPost_DB',
            'Remove_Original_QT',
        ]
    },
    'props': {
        'animatic_exchange': ANIMATIC_EXCHANGE,
        'client': 'monster',
        'editorial': ROOT_DIR,
        'program': 'monster'
    }
}