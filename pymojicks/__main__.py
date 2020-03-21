from argparse import ArgumentParser, FileType
from traceback import print_exc

import pymojicks

def core(parser, args):
    if args.version:
        return show_version()

    if args.filename is None:
        return run_repl()
    else:
        return run_code(args.filename)

def show_version():
    print('Version:', pymojicks.__version__)

def run_code(file):
    pymojicks.run(file.read())

def run_repl():
    while True:
        code = input('>>> ')
        try:
            pymojicks.run(code)
        except Exception as e:
            print_exc()

def parse_args():
    parser = ArgumentParser(description='The Official Emojicks Interpreter for Python.')

    parser.add_argument('filename', type=FileType('r', encoding='utf-8'), nargs='?', help='the name of the file to run.')
    parser.add_argument('-v', '--version', action='store_true', help='shows the version of PyMojicks installed.')
    parser.set_defaults(func=core)

    return parser, parser.parse_args()

def main():
    parser, args = parse_args()
    args.func(parser, args)

main()
