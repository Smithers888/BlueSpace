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

import itertools
import sys

_arithmap = {
    '\t   ': lambda x, y: x + y,
    '\t  \t': lambda x, y: x - y,
    '\t  \n': lambda x, y: x * y,
    '\t \t ': lambda x, y: x // y,
    '\t \t\t': lambda x, y: x % y,
    }

def getexecute(stmt):
    rep = stmt.rep
    param = stmt.param
    if param is not None:
        value = param.value
    
    # Stack instructions (' ')
    if rep == '  ': # Push
        def execute(machine):
            machine.stack.append(value)
    elif rep == ' \n ': # Duplicate
        def execute(machine):
            machine.stack.append(machine.stack[-1])
    elif rep == ' \t ': # Copy
        def execute(machine):
            machine.stack.append(machine.stack[-value-1])
    elif rep == ' \n\t': # Swap
        def execute(machine):
            machine.stack[-1], machine.stack[-2] = machine.stack[-2], machine.stack[-1]
    elif rep == ' \n\n': # Discard
        def execute(machine):
            machine.stack.pop()
    elif rep == ' \t\n': # Slide
        def execute(machine):
            del machine.stack[-value-1:-1]
    
    # Arithmetic instructions ('\t ')
    elif rep.startswith('\t '):
        operator = _arithmap[rep]
        def execute(machine):
            y = machine.stack.pop()
            machine.stack[-1] = operator(machine.stack[-1], y)
    
    # Heap instructions ('\t\t')
    elif rep == '\t\t ': # Store
        def execute(machine):
            y = machine.stack.pop()
            x = machine.stack.pop()
            machine.heap[x] = y
    elif rep == '\t\t\t': # Retrieve
        def execute(machine):
            machine.stack[-1] = machine.heap[machine.stack[-1]]
    
    # Flow control instructions ('\n')
    elif rep == '\n  ': # Label
        def execute(machine):
            pass
    elif rep == '\n \t': # Call
        def execute(machine):
            machine.calls.append(machine.pc)
            machine.pc = machine.findlabel(value)
    elif rep == '\n \n': # Jump
        def execute(machine):
            machine.pc = machine.findlabel(value)
    elif rep == '\n\t ': # JumpZero
        def execute(machine):
            if machine.stack.pop() == 0:
                machine.pc = machine.findlabel(value)
    elif rep == '\n\t\t': # JumpNegative
        def execute(machine):
            if machine.stack.pop() < 0:
                machine.pc = machine.findlabel(value)
    elif rep == '\n\t\n': # Return
        def execute(machine):
            machine.pc = machine.calls.pop()
    elif rep == '\n\n\n': # End
        def execute(machine):
            machine.pc = None
    
    # IO instructions ('\t\n')
    elif rep == '\t\n  ': # OutputChar
        def execute(machine):
            sys.stdout.write(chr(machine.stack.pop()))
    elif rep == '\t\n \t': # OutputNum
        def execute(machine):
            sys.stdout.write(str(machine.stack.pop()))
    elif rep == '\t\n\t ': # ReadChar
        def execute(machine):
            sys.stdout.flush()
            try:
                x = ord(sys.stdin.read(1))
            except EOFError:
                x = -1
            machine.heap[machine.stack.pop()] = x
    elif rep == '\t\n\t\t': # ReadNum
        def execute(machine):
            sys.stdout.flush()
            s = sys.stdin.readline()
            machine.heap[machine.stack.pop()] = int(s)
    
    return execute

class interpret:
    def __init__(self, stmt):
        self.execute = getexecute(stmt)
        self.label = stmt.param.value if stmt.rep == '\n  ' else None
        self.string = stmt.toassembly()

class machine:
    def __init__(self, program):
        self.program = [interpret(stmt) for stmt in program]
        self.stack = []
        self.heap = {}
        self.pc = -1
        self.calls = []
        self.inputqueue = ''
        self.labels = {stmt.label: i for stmt, i in zip(self.program, itertools.count())
                                     if stmt.label is not None}
    
    def findlabel(self, l):
        if l in self.labels:
            return self.labels[l]
        else:
            print('BlueSpace: Runtime error, label not found', file=sys.stderr)
            exit(1)
    
    def step(self):
        if self.pc is None:
            return False
        self.pc += 1
        try:
            self.program[self.pc].execute(self)
        except:
            if self.pc >= len(self.program):
                print('BlueSpace: Runtime error, unexpected end of code', file=sys.stderr)
            else:
                print('BlueSpace: Runtime error, cannot execute ' + self.program[self.pc].string, file=sys.stderr)
            exit(1)
        return True
