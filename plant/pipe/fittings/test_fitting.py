import os

from .base_fittings import IO_Fitting

class Test_Fitting(IO_Fitting):

    def fitting(self):
        print(f'test fitting 01 is printing that my path is {self.fso.path}')
        self.fso.props.yarp = "narp"
        print(self.fso.props)
        new_name = self.fso.name + "_gadzooks"
        new_path = os.path.join(self.fso.directory, new_name + self.fso.extension)
        os.rename(self.fso.path, new_path)
        self.fso.path = new_path
        print(f'test fitting 01 is printing that my path has been changed to {self.fso.path}')