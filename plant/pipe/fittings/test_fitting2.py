import os, shutil
import os.path as path

from .base_fittings import Fitting

class Test_Fitting2(Fitting):

    def fitting(self):
        new_path = "F:\\tmp\\dos"
        new_sub_dir = f'S{self.fso.props.sea}_SH{self.fso.props.shot}'
        new_path = path.join(self.fso.props.base_dir, new_sub_dir)
        if not path.isdir(new_path):
            os.makedirs(new_path)
        shutil.move(self.fso.path, path.join(new_path, self.fso.filename))