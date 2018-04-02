from auditor.base_exceptions import CompileException, RuntimeException
import operator

def transform_body(value, name, row, operator_func, other_key):
    # write the transform here
    second = row.get(other_key)
    return value if operator_func(value, second) else '<BAD_DATA>'

class OperatorCompileException(CompileException):
    pass

class OperatorRuntimeException(RuntimeException):
    pass

def compile_time_error(*args, **kwargs):
    """
    This should return a message that says what things you need
    in order to run your function
    """
    return """
    operator compile error
    operator takes two args:
    - an operator key
    - the column to compare against

    example:
    col example
    | operator lt other

    would mean that it would return the value of the column if (row[example] < row[other])
    and <BAD_DATA> otherwise

    a list of all valid operator names can be found at:
    https://docs.python.org/3/library/operator.html

    passed: {}
    """.format(*args, **kwargs)

def check_args(*args):
    """
    The date_parse transform takes no compile time args
    """
    if not len(args) == 3:
        raise OperatorCompileException(compile_time_error(*args))
    if not getattr(operator, args[1]):
        raise OperatorCompileException(*args)



def get_transform_function(*compile_args):
    func, operator_key, other_key = compile_args
    operator_func = getattr(operator, operator_key)

    def transform(*runtime_args):
        nonlocal operator_func
        try:
            return transform_body(*runtime_args, operator_func=operator_func, other_key=other_key)
        except Exception as ex:
            raise OperatorRuntimeException(ex)

    return transform
