from auditor.base_exceptions import CompileException, RuntimeException
import os
import yaml

def transform_body(value, name, row, whitelist_data):
    # write the transform here
    return value if not value in whitelist_data else '<BAD_DATA>'

class WhitelistCompileException(CompileException):
    pass

class WhitelistRuntimeException(RuntimeException):
    pass

def compile_time_error(*args, **kwargs):
    """
    This should return a message that says what things you need
    in order to run your function
    """
    return """
    whitelist compile error
    whitelist takes one arg corresponding to the file that is
    yaml, json or newline delimited consisting of valid values
    for the current column

    passed: {}
    """.format(*args, **kwargs)

def serialize(infile):
    """
    File formats include:
    yaml, json and newline delimited
    """
    text = infile.readlines()
    lines = [line.replace('\n', '') for line in text]
    try:
        data = yaml.load(text)
    except:
        data = lines
    return data


def check_args(*args):
    """
    The date_parse transform takes no compile time args
    """
    try:
        func = args[0]
        whitelist_file_path = args[1]
    except:
        raise WhitelistCompileException(compile_time_error(*args))
    if not os.path.isfile(whitelist_file_path):
        raise WhitelistCompileException("""
        Please pass a valid path to a json or yaml list or a newline delimited
        list of strings.
        path passed: {}
        current working directory: {}
        """.format(whitelist_file_path, os.getcwd()))
    try:
        with open(whitelist_file_path, 'r') as infile:
            data = serialize(infile)
    except:
        raise WhitelistCompileException("""
        The file passed to the whitelist is not parseable as yaml or json.
        Make sure you are referencing a properly formatted yaml or json file
        or a new line delimited list of strings.

        path passed: {}
        current working directory: {}
        """.format(whitelist_file_path, os.getcwd()))
    if not type(data) == type([]):
        raise WhitelistCompileException("""
        The file passed was parsed but was not a list.
        Make sure the file contents are properly formatted as yaml, json, or
        new line delimited.
        path passed: {}
        current working directory: {}
        """.format(whitelist_file_path, os.getcwd()))


def get_transform_function(*compile_args):
    func, whitelist_file_path = compile_args
    with open(whitelist_file_path, 'r') as infile:
        whitelist_data = serialize(infile)

    def transform(*runtime_args):
        nonlocal whitelist_data
        try:
            return transform_body(*runtime_args, whitelist_data=whitelist_data)
        except Exception as ex:
            raise WhitelistRuntimeException(ex)

    return transform
