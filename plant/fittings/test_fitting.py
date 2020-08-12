from .base_fittings import Fitting

class Test_Fitting(Fitting):

    def fitting(self):
        print(f'test fitting 01 is printing that my path is {self.fso.path}')