from auditor.base_exceptions import CompileException, RuntimeException

def transform_body(value, name, row):
    # write the transform here
    return value

class Strip_WhitespaceCompileException(CompileException):
    pass

class Strip_WhitespaceRuntimeException(RuntimeException):
    pass

def compile_time_error(*args, **kwargs):
    """
    This should return a message that says what things you need
    in order to run your function
    """
    return "strip_whitespace compile error".format(*args, **kwargs)

def check_args(*args):
    """
    The date_parse transform takes no compile time args
    """
    raise Strip_WhitespaceCompileException


def get_transform_function(*compile_args):

    def transform(*runtime_args):
        try:
            return transform_body(*runtime_args)
        except Exception as ex:
            raise Strip_WhitespaceRuntimeException(ex)

    return transform