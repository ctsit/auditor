import yaml

class ConfigParser(object):
    def __init__(self, path):
        with open(path, 'r') as infile:
            self.config_data = yaml.load(infile)

        self.columns = list(self.config_data.get('header_meaning').values())
        self.new_cols = self.config_data.get('new_headers').values()
        self.output_cols = self.config_data.get('headers')
        self.delimiter = self.config_data.get('csv_conf').get('delimiter')
        self.quote_char = self.config_data.get('csv_conf').get('quotechar')
        self.encoding = self.config_data.get('csv_encoding')

        self.whitelists = self.config_data.get('whitelist')
        self.blacklists = self.config_data.get('blacklist')
        self.lookups = self.config_data.get('lookups')

        self.mappings = self.config_data.get('mappings')

    def write(self, output_path):
        with open(output_path, 'w') as outfile:
            outfile.writelines(self.make_preamble())
            outfile.write('\n')
            outfile.writelines([self.make_col_block(mapping) for mapping in self.mappings])

    def make_preamble(self):
        lines = []
        lines.append("read data/claw.output")
        lines.append("write data/auditor.output")
        lines.append("separator {}".format(self.delimiter))
        lines.append("quotechar {}".format(self.quote_char))
        lines.append("encoding {}".format(self.encoding))
        lines.append(" ")
        lines.append("column_add {}".format(self.get_new_cols()))
        lines.append("column_order {}".format(" ".join(self.output_cols)))
        lines.append(" ")
        return "\n".join(lines)

    def make_col_block(self, mapping):
        col_name = mapping.get('header')
        maps = mapping.get('maps')
        lines = []
        lines.append("col {}".format(col_name))
        for item in maps:
            instruction = self.instruction_for_mapping(item, col_name, mapping)
            if instruction:
                lines.append("| {}".format(instruction))
        lines.append("| done")
        lines.append("\n")
        return '\n'.join(lines)


    def instruction_for_mapping(self, mapping, col, item):
        mappings = {
            'format_date': 'date_parse',
            'is_blacklist': 'blacklist',
            'is_whitelist': 'whitelist',
            'lookup': 'lookup',
            'strip_whitespace': 'strip_whitespace',
            'greater_equal': 'operator le',
        }
        try:
            if type(mapping) == type('string'):
                instruction = mappings.get(mapping)
            else:
                instruction = mappings.get(mapping['func'])
            if type(instruction) == type(None):
                return None
            args = self.lookup_args(instruction, col, mapping)
            return " ".join([instruction, args])
        except Exception as ex:
            return None

    def lookup_args(self, instruction, col, mapping):
        if instruction == 'date_parse' or instruction == 'strip_whitespace':
            return ""
        elif instruction == 'blacklist':
            return self.get_blacklist(col)
        elif instruction == 'whitelist':
            return self.get_whitelist(col)
        elif instruction == 'lookup':
            return self.get_lookup(col)
        elif instruction == 'operator le':
            return self.get_operator_le(col, mapping['args'])
        else:
            return ""


    def get_blacklist(self, col):
        path = [item['vals_file_path'] for item in self.blacklists if col == item['header_name']]
        return path[0]

    def get_whitelist(self, col):
        path = [item['vals_file_path'] for item in self.whitelists if col == item['header_name']]
        return path[0]

    def get_lookup(self, col):
        item = [item for item in self.lookups if col == item['header_name']]
        item = item[0]
        return " ".join([item.get('vals_file_path'), item.get('header_name')])

    def get_operator_le(self, col, args):
        return args[0]

    def get_new_cols(self):
        cols = [col.get('name') for col in self.new_cols]
        return ' '.join(cols)
