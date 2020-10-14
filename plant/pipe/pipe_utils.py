from typing import Type

from box import Box
from httpx import AsyncClient

from .fittings import *
from .filters import Filter
from .pipe import Pipe
from ..database.models import Client


def call_fitting(fitting:str):
    return globals()[fitting]

def init_filter(filter:str):
    return Filter(filter)

def init_Pipe(queues, callback, **kwargs):

    config = Box(kwargs)

    config.props.client = Client().new_or_get(config.props.client)
    filters = [init_filter(filter) for filter in config.filters]
    # fittings = [call_fitting(fitting) for fitting in config.fittings]
    fittings = {}

    for key in config.fittings:
        fittings[key] = [call_fitting(fitting) for fitting in config.fittings[key]]
    print(fittings)
    new_pipe = Pipe(
        name = config.name,
        dir = config.dir, 
        reject_dir  =config.reject_dir,
        queues = queues,
        filters = filters,
        fittings = fittings,
        props = config.props,
    )
    new_pipe.subscribe(callback)
    return new_pipe
