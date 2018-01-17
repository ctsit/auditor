from auditor.base_exceptions import CompileException, RuntimeException

def transform_body(value, name, row):
    return value

class DoneCompileException(CompileException):
    pass

class DoneRuntimeException(RuntimeException):
    pass

def compile_time_error(*args, **kwargs):
    """
    This should return a message that says what things you need
    in order to run your function
    """
    return """
    done compile error
    done command accepts no args
    """.format(*args, **kwargs)

def check_args(*args):
    """
    The done transform takes no compile time args
    and is what a column command should be finished with
    """
    if not (len(args) == 1 and args[0] == 'done'):
        raise DoneCompileException(compile_time_error(*args))


def get_transform_function(*compile_args):

    def transform(*runtime_args):
        try:
            return transform_body(*runtime_args)
        except Exception as ex:
            raise DoneRuntimeException(ex)

    return transform
