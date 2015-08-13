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

from assembler import assemble
from compiler import topython
from instructions import instructions
from interpreter import machine
from parser import parser

import argparse
import sys

argparser = argparse.ArgumentParser(description='''BlueSpace - A Whitespace interpreter in Python3.
For more information on Whitespace, visit http://compsoc.dur.ac.uk/whitespace/

author: Smithers888
''', epilog='Note: If using standard input for the source file with the --run or --runcompiled options, this will make it difficult to supply input to the program.', formatter_class=argparse.RawDescriptionHelpFormatter)
argparser.add_argument('-p', '--printable', action='store_true', help='use the characters `s`, `t` and `n` instead of space, tab and newline respectively')
actiongroup = argparser.add_mutually_exclusive_group()
actiongroup.add_argument('-a', '--assemble', action='store_true', help='assemble code to whitespace')
actiongroup.add_argument('-c', '--compile', action='store_true', help='compile whitespace to Python and print')
actiongroup.add_argument('-C', '--runcompiled', action='store_true', help='compile whitespace to Python and execute')
actiongroup.add_argument('-d', '--disassemble', action='store_true', help='disassemble Whitespace code instead of executing it')
actiongroup.add_argument('-r', '--run', action='store_true', help='run the Whitespace code (default)')
argparser.add_argument('-v', '--version', action='store_true', help='print version information and exit')
argparser.add_argument('sourcepath', nargs='?', default='-', help='path to the input source file, if omitted or `-\', use standard input')

args = argparser.parse_args()

if args.version:
    print('BlueSpace 1.0\nCopyright (C) 2014 Christopher Smith')
    sys.exit()

if not (args.assemble or args.compile or args.runcompiled or args.disassemble):
    args.run = True

if args.sourcepath == '-':
    sourcefile = sys.stdin
else:
    try:
        sourcefile = open(args.sourcepath, 'r')
    except OSError:
        print('BlueSpace: Failed to open ' + sourcefile, file=sys.stderr)
        sys.exit(1)

if args.assemble:
    try:
        code = assemble(sourcefile, args.printable)
    except RuntimeError:
        sys.exit(1)
    print(code, end='')
    sys.exit()

if args.printable:
    tr = {'s': ' ', 't': '\t', 'n': '\n'}
    source = ''.join((tr[x] for x in sourcefile.read() if x in tr))
else:
    source = ''.join((x for x in sourcefile.read() if x in ' \t\n'))

if args.disassemble:
    try:
        for stmt in parser(source).parse():
            print(stmt)
    except RuntimeError as err:
        sys.exit(err)
    sys.exit()

try:
    program = parser(source).parse()
except RuntimeError as err:
    sys.exit(err)

if args.compile:
    print(topython(program))
elif args.runcompiled:
    try:
        exec(topython(program))
    except SystemExit:
        pass
else:
    themachine = machine(program)
    while themachine.step():
        pass
