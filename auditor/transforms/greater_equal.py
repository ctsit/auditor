from auditor.base_exceptions import CompileException, RuntimeException

def transform_body(value, name, row, other_key):
    # write the transform here
    second = row.get(other_key)
    return value if value >= second else '<BAD_DATA>'

class GreaterEqualCompileException(CompileException):
    pass

class GreaterEqualRuntimeException(RuntimeException):
    pass

def compile_time_error(*args, **kwargs):
    """
    This should return a message that says what things you need
    in order to run your function
    """
    return """
    greater_equal compile error
    make sure you pass a key that equals the name of another column
    that you want to test against

    col >= other

    args passed: {}
    """.format(*args, **kwargs)

def check_args(*args):
    """
    The date_parse transform takes no compile time args
    """
    if not len(args) == 2:
        raise GreaterEqualCompileException(compile_time_error(*args))


def get_transform_function(*compile_args):
    func, other_key = compile_args

    def transform(*runtime_args):
        nonlocal other_key
        try:
            return transform_body(*runtime_args,
                                  other_key=other_key)
        except Exception as ex:
            raise GreaterEqualRuntimeException(ex)

    return transform
