from auditor.base_exceptions import CompileException, RuntimeException
import os
import yaml

def transform_body(value, name, row, key, lookup_data):
    lookup_key = row[key]
    value = lookup_data.get(lookup_key)
    return value

class LookupCompileException(CompileException):
    pass

class LookupRuntimeException(RuntimeException):
    pass

def compile_time_error(*args, **kwargs):
    """
    This should return a message that says what things you need
    in order to run your function
    """
    return """
    lookup requires two additional args:
      *  a path to a yaml or json file that is a dictionary
      *  the the name of the column from which to get the data to do a lookup
    passed args: {}
    """.format(*args, **kwargs)

def check_args(*args):
    """
    The date_parse transform takes no compile time args
    """
    try:
        func = args[0]
        lookup_file_path = args[1]
        key = args[2]
    except:
        raise LookupCompileException(compile_time_error(*args))
    if not os.path.isfile(lookup_file_path):
        LookupCompileException("""
        Please pass a valid path to a json or yaml dictionary
        path passed: {}
        current working directory: {}
        """.format(lookup_file_path, os.getcwd()))
    try:
        with open(lookup_file_path, 'r') as infile:
            data = yaml.load(infile)
    except:
        raise LookupCompileException("""
        The file passed to the lookup is not parseable as yaml or json.
        Make sure you are referencing a properly formatted yaml or json file
        with a dictionary of the lookup key and corresponding value.

        path passed: {}
        current working directory: {}
        """.format(lookup_file_path, os.getcwd()))
    if not type(data) == type({}):
        raise LookupCompileException("""
        The file passed was parsed but was not a dictionary.
        Make sure the file contents are properly formatted as yaml or json.
        path passed: {}
        current working directory: {}
        """.format(lookup_file_path, os.getcwd()))


def get_transform_function(*compile_args):
    func, lookup_file_path, key = compile_args
    with open(lookup_file_path, 'r') as infile:
        lookup_data = yaml.load(infile)

    def transform(*runtime_args):
        nonlocal lookup_data
        nonlocal key
        try:
            return transform_body(*runtime_args, key=key, lookup_data=lookup_data)
        except Exception as ex:
            raise LookupRuntimeException(ex)

    return transform
