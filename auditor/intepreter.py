from auditor.base_exceptions import RuntimeException
from auditor.column import Column
import csv
from copy import copy

class Interpreter(object):

    def __init__(self, program):
        self._program = program

    def get_instructions(self, operation, one_result=False, optional=False):
        if type(operation) == type(''):
            test = lambda i: i.get('op') == operation
        elif type(operation) == type([]):
            test = lambda i: i.get('op') in operation
        matching = [op for op in self._program if test(op)]
        if optional and len(matching) == 0:
            return None
        if one_result:
            if not len(matching) == 1:
                raise RuntimeException('Too many instances of instruction: {}'.format(matching))
            else:
                return matching[0]
        else:
            return matching


    def get_column_transforms(self):
        transforms = self.get_instructions(['col', '|'])
        indices = [transforms.index(item) for item in transforms if item.get('op') == 'col']
        indices.append(None)
        if len(indices) == 2:
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

    def get_args_for_op(self, operation, expected=1, one_result=False, optional=False):
        instructions = self.get_instructions(operation)
        ins_args = [item.get('args') for item in instructions]
        if optional and len(ins_args) == 0:
            return None
        if one_result:
            if not len(ins_args) == 1:
                raise RuntimeException('Too many instances of instruction: {}'.format(matching))
            else:
                if expected == 1:
                    return ins_args[0][0]
                elif expected == -1:
                    return ins_args[0]
        else:
            return ins_args

    def __call__(self):
        # build up how to read file
        inpath = self.get_args_for_op('read', one_result=True)
        outpath = self.get_args_for_op('write', one_result=True)
        encoding = self.get_args_for_op('encoding', one_result=True, optional=True)
        quotechar = self.get_args_for_op('quotechar', one_result=True, optional=True)
        separator = self.get_args_for_op('separator', one_result=True, optional=True)

        infile = open(inpath, 'r', encoding=encoding)
        outfile = open(outpath, 'w', encoding=encoding)

        # create reader for csv
        reader_opts = {
            'quotechar': quotechar[0] if len(quotechar) else None,
            'delimiter': separator[0] if len(separator) else None,
        }
        reader = csv.DictReader(infile, **reader_opts)

        # create writer for csv
        headers = copy(reader.fieldnames)
        renames = self.get_args_for_op('column_rename', optional=True)
        rename_lookup = {}
        for old, new in renames:
            rename_lookup[old] = new
            headers[headers.index(old)] = new
        column_order = self.get_args_for_op('column_order', expected=-1, one_result=True)
        headers = sorted(headers, key=lambda col: column_order.index(col))


        writer = csv.DictWriter(outfile, fieldnames=headers, **reader_opts)
        # write header
        writer.writeheader()

        # build up transforms for each column
        columns = self.get_column_transforms()

        # for each row
        for row in reader:
            new_row = {}
            for key, val in rename_lookup.items():
                row[val] = row[key]
                del row[key]
            for key in headers:
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
