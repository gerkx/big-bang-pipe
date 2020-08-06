from .fitting_state import Fitting_State



class DB_Fitting:
    def __init__(self, fso):
        self.state = Fitting_State()
        self.fso = fso