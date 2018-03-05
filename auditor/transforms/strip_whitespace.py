from auditor.base_exceptions import CompileException, RuntimeException

def transform_body(value, name, row):
    # write the transform here
    return str(value).strip()

class StripWhitespaceCompileException(CompileException):
    pass

class StripWhitespaceRuntimeException(RuntimeException):
    pass

def compile_time_error(*args, **kwargs):
    """
    This should return a message that says what things you need
    in order to run your function
    """
    return """
    strip_whitespace compile error.
    strip_whitespace takes no args.

    passed: {}
    """.format(*args, **kwargs)

def check_args(*args):
    """
    The date_parse transform takes no compile time args
    """
    if len(args):
        raise StripWhitespaceCompileException(compile_time_error(*args))


def get_transform_function(*compile_args):

    def transform(*runtime_args):
        try:
            return transform_body(*runtime_args)
        except Exception as ex:
            raise StripWhitespaceRuntimeException(ex)

    return transform
