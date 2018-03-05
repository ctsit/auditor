from auditor.base_exceptions import RuntimeException
from auditor.column_mapper import ColumnMapper
from auditor.row_mapper import RowMapper
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

        columns = []
        for instructions in transform_by_col:
            col_op = instructions[0]
            trans_ops = instructions[1:]
            col_name = col_op.get('args')[0]
            columns.append(ColumnMapper(instructions))
        columns.sort(key=lambda col: -1 * col.priority)
        return columns

    def get_args_for_op(self, operation, expected=1, one_result=False, optional=False):
        instructions = self.get_instructions(operation)
        ins_args = [item.get('args') for item in instructions]
        if optional and len(ins_args) == 0:
            return None
        if one_result:
            if not len(ins_args) == 1:
                raise RuntimeException('Too many instances of instruction: {}'.format(instructions))
            else:
                if expected == 1:
                    return ins_args[0][0]
                elif expected == -1:
                    return ins_args[0]
        else:
            return ins_args

    def get_infile_outfile_options(self):
        inpath = self.get_args_for_op('read', one_result=True)
        outpath = self.get_args_for_op('write', one_result=True)
        encoding = self.get_args_for_op('encoding', one_result=True, optional=True)
        quotechar = self.get_args_for_op('quotechar', one_result=True, optional=True)
        separator = self.get_args_for_op('separator', one_result=True, optional=True)

        infile = open(inpath, 'r', encoding=encoding)
        outfile = open(outpath, 'w', encoding=encoding)

        # create reader for csv
        options = {
            'quotechar': quotechar[0] if len(quotechar) else None,
            'delimiter': separator[0] if len(separator) else None,
        }
        return infile, outfile, options

    def get_outfile_header_information(self, reader):
        fieldnames = copy(reader.fieldnames)
        new_cols = self.get_args_for_op('column_add', one_result=True, expected=-1, optional=True)
        if new_cols:
            fieldnames += new_cols
        renames = self.get_args_for_op('column_rename', optional=True)
        rename_lookup = {}
        for old, new in renames:
            rename_lookup[old] = new
            fieldnames[fieldnames.index(old)] = new
        column_order = self.get_args_for_op('column_order', expected=-1, one_result=True)
        fieldnames = sorted(fieldnames, key=lambda col: column_order.index(col))
        return fieldnames, rename_lookup

    def __call__(self):
        infile, outfile, options = self.get_infile_outfile_options()
        reader = csv.DictReader(infile, **options)
        fieldnames, row_rename_mapping = self.get_outfile_header_information(reader)
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, **options)
        # write header
        writer.writeheader()

        # build up transforms for each column
        columns = self.get_column_transforms()

        # for each row
        for row in reader:
            mapper = RowMapper(row, row_rename_mapping, columns, fieldnames)
            for priority in mapper.get_priorities():
                mapper.update(priority)

            try:
                # check for bad data
                # writer.writerow(row)
                writer.writerow(mapper.data)
            except Exception as ex:
                print('Failed to write: {}'.format(mapper.data))
                print('Initial row: {}'.format(mapper._original_data))
                raise ex

        infile.close()
        outfile.close()
