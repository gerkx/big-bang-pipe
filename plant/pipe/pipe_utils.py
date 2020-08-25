from typing import Type

from box import Box
from .fittings import *

from .filters import Filter
from .pipe import Pipe

from httpx import AsyncClient

def call_fitting(fitting:str):
    return globals()[fitting]

def init_filter(filter:str):
    return Filter(filter)

def init_Pipe(queues, client:Type[AsyncClient], callback, **kwargs):
    config = Box(kwargs)
    filters = [init_filter(filter) for filter in config.filters]
    fittings = [call_fitting(fitting) for fitting in config.fittings]
    new_pipe = Pipe(
        name = config.name,
        dir = config.dir, 
        reject_dir  =config.reject_dir,
        queues = queues,
        client = client,
        filters = filters,
        fittings = fittings,
        props = config.props
    )
    new_pipe.subscribe(callback)
    return new_pipe
