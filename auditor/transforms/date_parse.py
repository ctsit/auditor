from auditor.base_exceptions import CompileException, RuntimeException
import dateutil.parser as date_parser

def transform_body(value, name, row):
    # write the transform here
    return date_parser.parse(value).strftime('%Y-%m-%d')

class DateParseCompileException(CompileException):
    pass

class DateParseRuntimeException(RuntimeException):
    pass

def compile_time_error(*args, **kwargs):
    """
    This should return a message that says what things you need
    in order to run your function
    """
    return """
    There should be no args passed to date_parse calls
    Args passed: {}
    """.format(*args, **kwargs)

def check_args(*args):
    """
    The date_parse transform takes no compile time args
    """
    if not ( len(args) == 1 and args[0] == 'date_parse' ):
        raise DateParseCompileException(compile_time_error(*args))


def get_transform_function(*compile_args):

    def transform(*runtime_args):
        try:
            return transform_body(*runtime_args)
        except Exception as ex:
            raise DateParseRuntimeException(ex)

    return transform
