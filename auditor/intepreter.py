from auditor.base_exceptions import RuntimeException
from auditor.column import Column
import csv

class Interpreter(object):

    def __init__(self, program):
        self._program = program

    def find_operation(self, operation, expected=1, optional=False):
        if type(operation) == type(''):
            test = lambda i: i.get('op') == operation
        elif type(operation) == type([]):
            test = lambda i: i.get('op') in operation
        if not optional:
            if expected == 1:
                ops = [item for item in self._program if test(item)]
                if len(ops) == expected:
                    return ops[0]
                else:
                    raise RuntimeException('Operation {} appears too many times'.format(operation))
            else:
                ops = [item for item in self._program if test(item)]
                if len(ops) == expected or expected == -1:
                    return ops
                else:
                    string = 'Operation {} appears the wrong number of times expected:{}, found:{}'.format(operation,
                                                                                                        expected,
                                                                                                        len(ops))
                    raise RuntimeException(string)
        else:
            return [item for item in self._program if test(item)]

    def get_column_transforms(self):
        transforms = self.find_operation(['col', '|'], expected=-1)
        indices = [transforms.index(item) for item in transforms if item.get('op') == 'col']
        if len(indices) == 1:
            transform_by_col = [transforms]
        else:
            transform_by_col = [transforms[indices[i]:indices[i+1]] for i in range(len(indices) - 1)]

        columns = {}
        for instructions in transform_by_col:
            col_op = instructions[0]
            trans_ops = instructions[1:]
            col_name = col_op.get('args')[0]
            columns.setdefault(col_name, Column(instructions))
        return columns

    def get_args_for_op(self, operation, expected=1, optional=False):
        operation = self.find_operation(operation, optional=optional)
        if type(operation) == type([]):
            args = [op.get('args') for op in operation]
            if not args:
                return args
            if len(args) == expected:
                if expected == 1:
                    return args[0]
                else:
                    return args
        elif type(operation) == type({}):
            args = operation.get('args')
            if len(args) == expected:
                if expected == 1:
                    return args[0]
            else:
                return args

    def __call__(self):
        # build up how to read file
        inpath = self.get_args_for_op('read')
        outpath = self.get_args_for_op('write')
        encoding = self.get_args_for_op('encoding', optional=True)
        quotechar = self.get_args_for_op('quotechar', optional=True)
        separator = self.get_args_for_op('separator', optional=True)

        if len(encoding) == 1:
            infile = open(inpath, 'r', encoding=encoding[0])
            outfile = open(outpath, 'w', encoding=encoding[0])
        else:
            infile = open(inpath, 'r')
            outfile = open(outpath, 'w')

        # create reader for csv
        reader_opts = {
            'quotechar': quotechar[0] if len(quotechar) else None,
            'delimiter': separator[0] if len(separator) else None,
        }
        reader = csv.DictReader(infile, **reader_opts)

        # create writer for csv
        headers = reader.fieldnames
        column_order = self.get_args_for_op('column_order', expected=-1)
        headers.sort(key=lambda col: column_order.index(col))

        writer = csv.DictWriter(outfile, fieldnames=headers, **reader_opts)
        # write header
        writer.writeheader()

        # build up transforms for each column
        columns = self.get_column_transforms()

        # for each row
        for row in reader:
            new_row = {}
            for key, value in row.items():
                # pass row through transforms
                try:
                    new_row.setdefault(key, columns[key](row))
                except KeyError:
                    raise RuntimeException('No column transform found for {}'.format(key))
                # write row to file
            try:
                writer.writerow(new_row)
            except:
                print('Failed to write: {}'.format(new_row))
                print('Initial row: {}'.format(row))

        # end
        infile.close()
        outfile.close()
