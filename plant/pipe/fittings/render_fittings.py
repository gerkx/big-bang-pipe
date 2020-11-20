import os, shutil
from datetime import datetime
import os.path as path
from typing import Type

import fileseq

from .base_fittings import IO_Fitting

from ...database.models import (
    Client, Project, Shot, Compo, Grade, WorkingPost
)

class Detect_Img_Sequence(IO_Fitting):
    def fitting(self):
        
        