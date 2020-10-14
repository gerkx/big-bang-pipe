from peewee import OperationalError

from .models import (
    Client, Project, Shot, AudioGrab, Music, Mix, Stem, WorkingAudio, 
    Asana_Project, Asana_Tag, Asana_Task, Asana_User
)


try:
    Client.create_table()
except OperationalError:
    print('Client table already exists')
try:
    Project.create_table()
except OperationalError:
    print('Project table already exists')
try:
    Shot.create_table()
except OperationalError:
    print('Shot table already exists')
try:
    AudioGrab.create_table()
except OperationalError:
    print('AudioGrab table already exists')
try:
    Music.create_table()
except OperationalError:
    print('Music table already exists')
try:
    Mix.create_table()
except OperationalError:
    print('Mix table already exists')
try:
    Stem.create_table()
except OperationalError:
    print('Stem table already exists')
try:
    WorkingAudio.create_table()
except OperationalError:
    print('WorkingAudio table already exists')
try:
    Asana_User.create_table()
except OperationalError:
    print('Asana_User table already exists')
try:
    Asana_Task.create_table()
except OperationalError:
    print('Asana_Task table already exists')
try:
    Asana_Project.create_table()
except OperationalError:
    print('Asana_Project table already exists')
try:
    Asana_Tag.create_table()
except OperationalError:
    print('Asana_Tag table already exists')