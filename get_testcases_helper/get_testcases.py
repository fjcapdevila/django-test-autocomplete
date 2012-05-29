#!/usr/bin/env python
import sys
from ast import parse, ClassDef, FunctionDef

_CASES = {}


def get_testunits(case):
    units = []
    for node in case.body:
        if isinstance(node, FunctionDef) and node.name.startswith('test_'):
            units.append(node)
    return units


def read_file(fname):
    if fname.endswith('.pyc'):
        return
    if not fname.endswith('.py'):
        fname = fname + '.py'
    try:
        return file(fname).read()
    except IOError:
        return


def run(argv):
    if len(argv) > 1:
        source = read_file(argv[1])
        if source is not None:
            data = parse(source)
            for node in data.body:
                if isinstance(node, ClassDef):
                    _CASES[node.name] = node

            which_prefix = '--units='
            if len(argv) > 2 and argv[-1].startswith(which_prefix):
                units_for = argv[-1][len(which_prefix):]
                if '.' in units_for:
                    cname, tname_prefix = units_for.split('.', 1)
                    for test in get_testunits(_CASES[cname]):
                        if test.name.startswith(tname_prefix):
                            print '%s.%s' % (cname, test.name)
                else:
                    # Shouldnt reach here
                    pass
            else:
                for case in _CASES.keys():
                    print case.name


if __name__ == '__main__':
    run(sys.argv)