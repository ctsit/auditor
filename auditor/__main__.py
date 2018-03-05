docstr = """
Auditor

Usage: auditor (<program_path>)

Options:
  -h --help                                     show this message and exit


Auditor is used to run auditor program files to alter csv files
"""
from docopt import docopt

from auditor.compiler import AuditorCompiler
from auditor.interpreter import Interpreter

def main(args=docopt(docstr)):
    program_path = args['<program_path>']
    compiler = AuditorCompiler()
    instructions = compiler(program_path)
    interpreter = Interpreter(instructions)
    interpreter()

if __name__ == '__main__':
    args = docopt(docstr)
    main(args)
    exit()
