from auditor.base_exceptions import CompileException, RuntimeException

def transform_body(value, name, row):
    # write the transform here
    return value

class GreaterThanCompileException(CompileException):
    pass

class GreaterThanRuntimeException(RuntimeException):
    pass

def compile_time_error(*args, **kwargs):
    """
    This should return a message that says what things you need
    in order to run your function
    """
    return "greater_than compile error".format(*args, **kwargs)

def check_args(*args):
    """
    The date_parse transform takes no compile time args
    """
    raise GreaterThanCompileException


def get_transform_function(*compile_args):

    def transform(*runtime_args):
        try:
            return transform_body(*runtime_args)
        except Exception as ex:
            raise GreaterThanRuntimeException(ex)

    return transform