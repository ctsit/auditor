import importlib
from auditor.base_exceptions import RuntimeException

class Column(object):
    def __init__(self, instructions):
        self.name = instructions[0].get('args')[0]
        try:
            self.priority = int(instructions[0].get('args')[1])
        except:
            self.priority = 999
        self.transforms = []
        for instruction in instructions[1:]:
            self.__set_transform(instruction)

    def __repr__(self):
        return '<name:{name};priority:{priority}>'.format(name=self.name, priority=self.priority)

    def __set_transform(self, instruction):
        if instruction.get('op') == '|':
            func = instruction.get('args')[0]
            args = instruction.get('args')
            if not func == 'return':
                transform = importlib.import_module('auditor.transforms.{}'.format(args[0]))
                self.transforms.append(transform.get_transform_function(*args))
            else:
                self.transforms.append(lambda value, name, row: value)
        else:
            raise RuntimeException('incorrect instruction sent to column {}'.format(instruction))


    def __call__(self, row):
        self.__original_value = row.get(self.name)
        value = self.__original_value
        for transform in self.transforms:
            value = transform(value, self.name, row)
        return value
