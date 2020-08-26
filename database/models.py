import datetime

# from nanoid import generate
from peewee import (Model, SqliteDatabase, 
    AutoField, CharField, DateTimeField, UUIDField, IntegerField, 
    ForeignKeyField, FloatField, BooleanField
)


db = SqliteDatabase('temp.db')
# PORTED
class BaseModel(Model):
    id = AutoField()
    guid = UUIDField()
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.date.now, null=True)
    
    class Meta:
        database = db

class User(Model):
    guid = UUIDField()
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    asana_id = CharField(null=True, unique=True)
    skype = CharField(null=True)
    phone = CharField(null=True)
    shotgun = CharField(null=True)

    class Meta:
        database = db

# PORTED
class Client(BaseModel):
    name = CharField()

# PORTED
class Project(BaseModel):
    client = ForeignKeyField(Client, backref='projects')
    name = CharField()
    production_number:int = IntegerField(null=True)
    emission_number:int = IntegerField(null=True)

# PORTED
class Shot(BaseModel):
    project = ForeignKeyField(Project, backref='shots')
    name = CharField(null=True)
    shot = IntegerField()
    sequence = IntegerField(null=True)
    duration = IntegerField(null=True)
    framerate = FloatField(null=True)

class VisModel(BaseModel):
    location = CharField()
    name = CharField()
    inbound_name = CharField()
    duration = IntegerField(null=True)
    frames = CharField(null=True)

class RenderSeq(VisModel):
    shot = ForeignKeyField(Shot, backref='renders')
    transcode_name = CharField(null=True)
    transcode_location = CharField(null=True)
    transcode_link = CharField(null=True)
    mp4_name = CharField(null=True)
    mp4_location = CharField(null=True)
    mp4_link = CharField(null=True)

class Grade(VisModel):
    shot = ForeignKeyField(Shot, backref='grades')

class Compo(VisModel):
    shot = ForeignKeyField(Shot, backref='compos')

class WorkingVis(BaseModel):
    # shot = ForeignKeyField(Shot, backref='int_viz')
    name = CharField()
    location = CharField()
    link = CharField(null=True)
    render = ForeignKeyField(RenderSeq, backref='int_renders')
    grade = ForeignKeyField(Grade, backref='int_grades', null=True)
    compo = ForeignKeyField(Compo, backref='int_compos', null=True)

# PORTED
class AudioModel(BaseModel):
    name = CharField()
    inbound_name = CharField()
    location = CharField()
    mp3_name = CharField(null=True)
    mp3_location = CharField(null=True)
    mp3_link = CharField(null=True)

class AudioGrab(AudioModel):
    project = ForeignKeyField(Project, backref='audio_grabs')
    lang = CharField(null=True)

class Music(AudioModel):
    project = ForeignKeyField(Project, backref='music')

class Mix(AudioModel):
    project = ForeignKeyField(Project, backref='mixes')
    lang = CharField(null=True)

class Stem(AudioModel):
    project = ForeignKeyField(Project, backref='stems')
    lang = CharField(null=True)

class WorkingAudio(BaseModel):
    name = CharField()
    location = CharField()
    link = CharField(null=True)
    grab = ForeignKeyField(AudioGrab, backref='int_grabs', null=True)
    music = ForeignKeyField(Music, backref='int_music', null=True)
    mix = ForeignKeyField(Mix, backref='int_mix', null=True)
    stem = ForeignKeyField(Stem, backref='int_stems', null=True)

class PProProj(BaseModel):
    name = CharField()
    documentID = CharField(null=True)
    location = CharField(null=True)
    link = CharField(null=True)
    project = ForeignKeyField(Project, backref='ppro', null=True)

class PProSeq(BaseModel):
    project = ForeignKeyField(PProProj, backref='sequences')
    name = CharField()
    sequenceID = CharField(null=True)

class Master(BaseModel):
    name = CharField()
    location = CharField()
    link = CharField(null=True)
    project = ForeignKeyField(Project, backref='masters', null=True)
    src_sequence = ForeignKeyField(PProSeq, backref='masters', null=True)
    rtve = BooleanField(default=False)
    pgs = BooleanField(default=False)
    cat = BooleanField(default=False)
    internal = BooleanField(default=False)
    chan_01 = CharField(null=True)
    chan_02 = CharField(null=True)
    chan_03 = CharField(null=True)
    chan_04 = CharField(null=True)
    chan_05 = CharField(null=True)
    chan_06 = CharField(null=True)
    chan_07 = CharField(null=True)
    chan_08 = CharField(null=True)
    chan_09 = CharField(null=True)
    chan_10 = CharField(null=True)
    chan_11 = CharField(null=True)
    chan_12 = CharField(null=True)
    chan_13 = CharField(null=True)
    chan_14 = CharField(null=True)
    chan_15 = CharField(null=True)
    chan_16 = CharField(null=True)

class Export(BaseModel):
    name = CharField()
    location = CharField()
    link = CharField(null=True)
    project = ForeignKeyField(Project, backref='exports', null=True)
    shot = ForeignKeyField(Shot, backref='exports', null=True)
    master = ForeignKeyField(Master, backref='exports', null=True)
    wip = BooleanField(default=False)
    lineal = BooleanField(default=False)
    tripartito = BooleanField(default=False)
    animatic_planos = BooleanField(default=False)
    music_ref = BooleanField(default=False)
    mix_ref = BooleanField(default=False)

    src_file = CharField(null=True)
    src_sequence = ForeignKeyField(PProSeq, backref='exports', null=True)




    
    
    

    


    








    



# class Working_Ftg(BaseModel)









    



