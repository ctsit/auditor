from copy import copy
import auditor.base_exceptions as base_ex

class RowMapper(object):
    def __init__(self, data, header_out_mapping, cols, target_fieldnames):
        self._original_data = copy(data)
        self._header_out_mapping = copy(header_out_mapping)
        self.target_fieldnames = target_fieldnames
        self.data = self.change_headers(self._original_data, self._header_out_mapping)
        self.cols = cols
        self._updates = []

    def change_headers(self, original, mapping):
        data = copy(original)
        for old, new in mapping.items():
            data[new] = copy(data[old])
            del data[old]
        return data

    def get_priorities(self):
        return [col.priority for col in self.cols]

    def get_output_keys(self):
        return self.target_fieldnames

    def get_output_data(self):
        retval = {}
        for key in self.get_output_keys():
            retval[key] = self.data[key]
        return retval

    def update(self, priority):
        matching_cols = [col for col in self.cols if col.priority == priority]
        data_copy = copy(self.data)
        for col in matching_cols:
            key = col.name
            if key in self.get_output_keys():
                data_copy[key] = col(data_copy)
            else:
                print(list(self.get_output_keys()))
                raise base_ex.CompileException("""
                There is a "col" block with a key that does not exist in the
                output csv. Either delete this block or add the column to the
                output with the "column_add" instruction.

                offending col: {}
                """.format(key))
        self.data = data_copy

    def has_bad_data(self):
        return '<BAD_DATA>' in self.data.values()
