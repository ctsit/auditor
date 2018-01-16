from copy import copy
import importlib

class Column(object):
    def __init__(self, compiled_column, row, output_name=None):
        self._compiled_column = copy(compiled_column)
        self.name = compiled_column.get('name')
        self.output_name = output_name or header
        self.__row = copy(row)
        self.transforms = []

    def get_serializable(self):
        return {
            'compilation_object': self._compiled_column,
            'intial_row': self.__row
        }

    def add_transform(self, transform_name, *compile_args):
        # we dont want a whole bunch of different functions and compilation
        # objects that are all going to be the same except for the row

        transform = importlib.import_module(tranform_name, 'auditor.transforms')
        self.transforms.append(transform.get_transform_function(*compile_args))
        pass
