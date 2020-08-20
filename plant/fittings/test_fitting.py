import os

from .base_fittings import Fitting

class Test_Fitting(Fitting):

    def fitting(self):
        print(f'test fitting 01 is printing that my path is {self.fso.path}')
        self.fso.props.yarp = "narp"
        print(self.fso.props)
        new_name = "gadzooks"
        new_path = os.path.join(self.fso.directory, new_name + self.fso.extension)
        os.rename(self.fso.path, new_path)
        self.fso.path = new_path
        print(f'test fitting 01 is printing that my path is {self.fso.path}')