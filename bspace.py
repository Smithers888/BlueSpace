#!/usr/bin/env python3

# Copyright (C) 2014 Christopher Smith
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name of the author shall not be used
# in advertising or otherwise to promote the sale, use or other dealings in
# this Software without prior written authorization from the author.

import assembler
from compiler import topython
from instructions import instructions
from interpreter import machine
from optimiser import optimise
from wsparser import parser

import argparse
import sys

argparser = argparse.ArgumentParser(description='''BlueSpace - A Whitespace interpreter in Python3.
For more information on Whitespace, visit http://compsoc.dur.ac.uk/whitespace/
''', formatter_class=argparse.RawDescriptionHelpFormatter)
argparser.add_argument('-v', '--version', action='store_true', help='print version information and exit')
argparser.add_argument('-i', '--input', choices=('whitespace', 'printable', 'assembly'), help="choose the input syntax, SYNTAX is `whitespace', `printable' or `assembly' (defaults to whitespace)", metavar='SYNTAX')
actiongroup = argparser.add_mutually_exclusive_group()
actiongroup.add_argument('-c', '--convertto', choices=('whitespace', 'printable', 'assembly', 'python', 'optimised'), help="if TARGET is `whitespace', `printable' or `assembly', convert to that syntax; if TARGET is `python' or `optimised', compile to Python3 source, respectively without or with optimisations", metavar='TARGET')
actiongroup.add_argument('-r', '--run', choices=('interpret', 'python', 'optimised'), help="if MODE is `interpret', interpret Whitespace code directly; if MODE is `python' or `optimised', compile as with -c MODE and then evaluate the resulting code (defaults to interpret)", metavar='MODE')
argparser.add_argument('sourcepath', nargs='?', default='-', help="path to the input source file, if omitted or `-', use standard input", metavar='SOURCE')

args = argparser.parse_args()

if args.version:
    print('BlueSpace 1.1\nCopyright (C) 2014 Christopher Smith')
    sys.exit()

if args.sourcepath == '-':
    sourcefile = sys.stdin
else:
    try:
        sourcefile = open(args.sourcepath, 'r')
    except OSError:
        print('BlueSpace: Failed to open ' + sourcefile, file=sys.stderr)
        sys.exit(1)

if args.input == 'assembly':
    try:
        program = list(assembler.parse(sourcefile))
    except RuntimeError:
        sys.exit(1)
else:
    if args.input == 'printable':
        tr = {'s': ' ', 't': '\t', 'n': '\n'}
        source = ''.join(tr[x] for x in sourcefile.read() if x in tr)
    else:
        source = ''.join(x for x in sourcefile.read() if x in ' \t\n')
    try:
        program = parser(source).parse()
    except RuntimeError as err:
        sys.exit(err)

if args.convertto == 'whitespace':
    for stmt in program:
        print(stmt.towhitespace(), end='')
elif args.convertto == 'printable':
    for stmt in program:
        print(stmt.toprintable())
elif args.convertto == 'assembly':
    for stmt in program:
        print(stmt.toassembly())
elif args.convertto == 'python':
    print(topython(program))
elif args.convertto == 'optimised':
    print(optimise(program))
elif args.run == 'python':
    try:
        exec(topython(program))
    except SystemExit:
        pass
elif args.run == 'optimised':
    try:
        exec(optimise(program))
    except SystemExit:
        pass
else:
    themachine = machine(program)
    while themachine.step():
        pass
