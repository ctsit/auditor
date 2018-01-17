import os
import importlib
from auditor.base_exceptions import CompileException

class AuditorCompiler(object):
    version = '1'
    operator_tokens = [
        'read',
        'encoding',
        'separator',
        'quotechar',
        'write',
        'column_add',
        'column_order',
        'column_rename',
        # 'row_sort',
        'col',
        '|',
    ]

    def __init__(self):
        pass

    def __call__(self, program_file_path):
        self.program_file_path = program_file_path
        with open(program_file_path, 'r') as program_file:
            self.code = program_file.read()

        self.parsed = self.tokenize_parse(self.code)
        self.validate(self.parsed)
        return self.parsed

    def tokenize_parse(self, code):
        lines = code.splitlines()
        operations = []
        current_operation = None
        for index, line in enumerate(lines):

            if '"' in line and not 'quotechar' in line:
                items = line.split('"')
                tokens = []
                for ind, item in enumerate(items):
                    if ind % 2 == 0:
                        tokens += item.split()
                    else:
                        tokens += [item]
            else:
                tokens = line.split()

            for token in tokens:
                if token in AuditorCompiler.operator_tokens:
                    current_operation = token
                    operations.append({
                        'op': token,
                        'line_num': index + 1,
                        'args': []
                    })
                else:
                    operations[-1]['args'].append(token)
        return operations

    def __check_file(self, *args):
        if len(args) == 1:
            if os.path.isfile(args[0]):
                pass
            else:
                raise CompileException('No file found at {}'.format(args[0]))
        else:
            raise CompileException('Wrong number of args, {}'.format(args))

    def __get_has_num_args(self, num=-1, greater_equal=-1, less_equal=-1):
        test = None
        if num > -1:
            test = lambda l: len(l) == num
        elif greater_equal > -1:
            test = lambda l: len(l) >= greater_equal
        elif less_equal > -1:
            test = lambda l: len(l) <= less_equal
        def check(*args):
            if test(args):
                pass
            else:
                raise CompileException('Wrong number of args, {}'.format(len(args)))
        return check

    def validate(self, parsed):
        op_args = [(item.get('op'), item.get('args'), item.get('line_num'))
                   for item in parsed]
        for operation, args, line_num in op_args:
            try:
                if operation == 'read':
                    self.__check_file(*args)
                elif operation in ['encoding', 'separator', 'quotechar', 'write']:
                    check = self.__get_has_num_args(num=1)
                    check(*args)
                elif operation == 'column_add':
                    check = self.__get_has_num_args(greater_equal=1)
                    check(*args)
                elif operation == 'column_rename':
                    check = self.__get_has_num_args(num=2)
                    check(*args)
                # elif operation in ['column_order', 'row_sort', '|']:
                elif operation in ['column_order', '|']:
                    check = self.__get_has_num_args(greater_equal=1)
                    check(*args)
                elif operation == '|':
                    check = self.__get_has_num_args(num=1)
                    check(*args)
                    try:
                        transform = importlib.import_module('auditor.transforms.{}'.format(args[0]))
                    except:
                        raise CompileException('No such transform module for function {}'.format(args[0]))
                    transform.check_args(*args)

            except Exception as ex:
                print('CompileException on line {}'.format(line_num))
                raise ex

