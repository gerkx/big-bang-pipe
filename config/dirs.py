import os
import os.path as path

ROOT_DIR = path.dirname(path.abspath(os.curdir))

INBOX_DIR = path.join(ROOT_DIR, '_inbox')

REJECT_INBOX = path.join(INBOX_DIR, '_reject')

AUDIO_INBOX = path.join(INBOX_DIR, 'audio')

