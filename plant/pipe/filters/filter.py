import re
from itertools import zip_longest
from string import Template
from typing import Type


class Filter:
    def __init__(self, template: dict):
        self.name:str = template['name']
        self.template:str =  template['template']
        self.definitions:dict = template['definitions']
        self.slice_idxs = self.create_slice_idxs()


    def match(self, name):
        return False if not self.run_re(name) else True

    def extract_vals(self, name) -> dict:
        if not self.match(name):
            return None
        else:
            idxs = self.create_slice_idxs()
            keys:list = [
                key.replace('${', '').replace('}', '') for key in
                [f'{self.template[idx[0]:idx[1]]}' for idx in idxs]
            ]
            key_val:dict = {}
            re_matches = self.run_re(name)
            for idx, key in enumerate(keys):
                key_val[key] = re_matches[idx]
            return key_val
    
    @staticmethod
    def convert_template_to_key(chunk:str) -> str:
        return chunk[2:len(chunk)-1]

    def create_slice_idxs(self) -> list:
        chunks = [*re.finditer(
            r'\${\w*\}',
            self.template,
            re.IGNORECASE
        )]
        return [[match.start(0), match.end(0)] for match in chunks]

    def create_static_chunks(self) -> list:
        static:list = []
        for idx, _ in enumerate(self.slice_idxs):
            if idx == 0:
                static.append(self.template[0:self.slice_idxs[idx][0]])
            else:
                static.append(self.template[self.slice_idxs[idx-1][1]:self.slice_idxs[idx][0]])
        end_idx:int = self.slice_idxs[len(self.slice_idxs)-1][1]
        if end_idx != len(self.template):
            static.append(self.template[end_idx:])
        return static

    def create_re_chunks(self) -> list:
        return [ 
            self.create_subpattern(self.convert_template_to_key(chunk))
            for chunk in [f'{self.template[idx[0]:idx[1]]}' for idx in self.slice_idxs]
        ]

    def create_subpattern(self, key:str) -> str:
        tipo = self.definitions[key]['type']
        opts = self.definitions[key]['options']

        min_len = opts['min_length'] - 1 if 'min_length' in opts else ''
        max_len = opts['max_length'] - 1 if 'max_length' in opts else ''
        
        if tipo == 'alpha_numeric':
            pattern = r'\w'
        elif tipo == 'alpha':
            pattern = r'\w[^0-9]'
        else:
            pattern = r'\d'
            min_len = opts['min_length'] if 'min_length' in opts else ''
            max_len = opts['max_length'] if 'max_length' in opts else ''
        
        if self.template.startswith('${' + key + '}'):
            pattern = '^' + pattern

        pattern += "{" + str(min_len) + "," + str(max_len) + "}"
        
        if self.template.endswith('${' + key + '}'):
            pattern += '$'
        return pattern
        

    def create_re_pattern(self) -> str:
        idxs:list = self.create_slice_idxs()
        reg:list = [
            self.create_subpattern(self.convert_template_to_key(template))
            for template in [f'{self.template[i[0]:i[1]]}' for i in idxs]
        ]
        static:list = []
        for idx, _ in enumerate(idxs):
            if idx == 0:
                static.append(self.template[0:idxs[idx][0]])
            else:
                static.append(self.template[idxs[idx-1][1]:idxs[idx][0]])
        end_idx:int = idxs[len(idxs)-1][1]
        if end_idx != len(self.template):
            static.append(self.template[end_idx:])
        zipped_lists = zip_longest(static, reg, fillvalue='')
        static, reg = zip(*zipped_lists)
        regex_pattern:str = r''
        for idx, substr in enumerate(static):
            regex_pattern += substr
            regex_pattern += reg[idx]
        return regex_pattern

    def run_re(self, name) -> list:
        zipped_lists = zip_longest(
            self.create_static_chunks(),
            self.create_re_chunks(),
            fillvalue=''
        )
        static, reg = zip(*zipped_lists)
        regex_pattern:str = r''
        for idx, substr in enumerate(static):
            regex_pattern += substr
            if len(reg) > 0:
                regex_pattern += f'({reg[idx]})'

        re_matches = re.match(regex_pattern, name, re.IGNORECASE)
        return None if re_matches is None else [*re_matches.groups()]



