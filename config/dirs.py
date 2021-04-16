import os
import os.path as path

TEST_DIR = 'Z:\\test'
ROOT_DIR = TEST_DIR
# ROOT_DIR = path.dirname(path.abspath(os.curdir))

MONSTER_DIR = path.abspath(path.join(ROOT_DIR, '..', '..', ))

ANIMATIC_EXCHANGE = path.abspath(
    path.join(MONSTER_DIR, 'EXCHANGE', 'BBB-Finales', 'Animatic')
)

INBOX_DIR = path.join(ROOT_DIR, '_inbox')

REJECT_INBOX = path.join(INBOX_DIR, '_reject')

AUDIO_INBOX = path.join(INBOX_DIR, 'audio')

POST_INBOX = path.join(INBOX_DIR, 'post')

RENDER_INBOX = path.join(INBOX_DIR, 'render')

EDITORIAL_INBOX = path.join(INBOX_DIR, 'editorial')

ANIMATIC_INBOX = path.join(EDITORIAL_INBOX, 'animatic')

# SERVER_DIR = 'Z:\\tmpServer'
SERVER_DIR = path.join(TEST_DIR, 'tmpServer')
