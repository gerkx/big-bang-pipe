from typing import Optional

import httpx
import json
import asyncio
from fastapi import FastAPI

from plant import Plant
from config import config

plant = Plant(config)

plant.start()


app = FastAPI()

@app.get('/')
def read_root():
    return { 'yo': 'sup?' }