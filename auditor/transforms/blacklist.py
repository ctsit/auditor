from auditor.base_exceptions import CompileException, RuntimeException
import os
import yaml

def transform_body(value, name, row, blacklist_data):
    # write the transform here
    return value if value in blacklist_data else '<BAD_DATA>'

class BlacklistCompileException(CompileException):
    pass

class BlacklistRuntimeException(RuntimeException):
    pass

def compile_time_error(*args, **kwargs):
    """
    This should return a message that says what things you need
    in order to run your function
    """
    return """
    blacklist compile error
    blacklist takes one arg corresponding to the file that is
    yaml, json or newline delimited consisting of invalid values
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
        blacklist_file_path = args[1]
    except:
        raise BlacklistCompileException(compile_time_error(*args))
    if not os.path.isfile(blacklist_file_path):
        raise BlacklistCompileException("""
        Please pass a valid path to a json or yaml list or a newline delimited
        list of strings.
        path passed: {}
        current working directory: {}
        """.format(blacklist_file_path, os.getcwd()))
    try:
        with open(blacklist_file_path, 'r') as infile:
            data = serialize(infile)
    except:
        raise BlacklistCompileException("""
        The file passed to the blacklist is not parseable as yaml or json.
        Make sure you are referencing a properly formatted yaml or json file
        or a new line delimited list of strings.

        path passed: {}
        current working directory: {}
        """.format(blacklist_file_path, os.getcwd()))
    if not type(data) == type([]):
        raise BlacklistCompileException("""
        The file passed was parsed but was not a list.
        Make sure the file contents are properly formatted as yaml, json, or
        new line delimited.
        path passed: {}
        current working directory: {}
        """.format(blacklist_file_path, os.getcwd()))


def get_transform_function(*compile_args):
    func, blacklist_file_path = compile_args
    with open(blacklist_file_path, 'r') as infile:
        blacklist_data = serialize(infile)

    def transform(*runtime_args):
        nonlocal blacklist_data
        try:
            return transform_body(*runtime_args, blacklist_data=blacklist_data)
        except Exception as ex:
            raise BlacklistRuntimeException(ex)

    return transform
