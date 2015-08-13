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

_arithmap = {
    '\t   ': '+',
    '\t  \t': '-',
    '\t  \n': '*',
    '\t \t ': '//',
    '\t \t\t': '%',
    }

class _optimiser:
    def __init__(self):
        self.result = [
            '#!/usr/bin/env python3',
            'import sys',
            'stack = []',
            'heap = {}',
            'def run(f):',
            '    while f is not None:',
            '        f = f()',
            'def start():',
            ]
        self.xvars = []
        self.reachable = True
        self.needpass = True
        self.checkheap = False
    
    def _stackval(self, i):
        j = len(self.xvars) - i - 1
        if j >= 0:
            if self.xvars[j] == None:
                return 'x' + str(j)
            else:
                return self.xvars[j]
        else:
            return 'stack[' + str(j) + ']'
    
    def _stackvar(self, i):
        j = len(self.xvars) - i - 1
        if j >= 0:
            return 'x' + str(j)
        else:
            return 'stack[' + str(j) + ']'
    
    def _dumpxs(self):
        for i in range(len(self.xvars) - 1, -1, -1):
            self.result.append('    stack.append(' + self._stackval(i) + ')')
        self.xvars.clear()
        self.checkheap = False
    
    def _dumpxs2(self):
        for i in range(len(self.xvars) - 1, -1, -1):
            self.result.append('        stack.append(' + self._stackval(i) + ')')
    
    def addstatement(self, stmt):
        rep = stmt.rep
        
        if not self.reachable:
            if rep == '\n  ': # Label
                self.xvars.clear()
                self.result.append('def ' + stmt.param.name() + '():')
                self.reachable = True
                self.needpass = True
            return
        
        if self.needpass:
            self.needpass = False
            if rep == '\n\t\n': # Return
                self.result.append('    pass')
                self.reachable = False
                return
        
        if rep == '  ': # Push
            self.xvars.append(str(stmt.param.value))
        elif rep == ' \n ': # Duplicate
            if len(self.xvars) == 0:
                self.xvars.append('stack[-1]')
            elif self.xvars[-1] is None:
                self.result.append('    x' + str(len(self.xvars)) + ' = ' + self._stackval(0))
                self.xvars.append(None)
            else:
                self.xvars.append(self.xvars[-1])
        elif rep == ' \t ': # Copy
            value = stmt.param.value
            if len(self.xvars) <= value or self.xvars[-1 - value] is None:
                self.result.append('    x' + str(len(self.xvars)) + ' = ' + self._stackval(value))
                self.xvars.append(None)
            else:
                self.xvars.append(self.xvars[-1 - value])
        elif rep == ' \n\t': # Swap
            if len(self.xvars) == 0:
                self.result.append('    stack[-1], stack[-2] = stack[-2], stack[-1]')
            elif len(self.xvars) == 1:
                self.result.append('    x0, stack[-1] = stack[-1], ' + self._stackval(0))
                self.xvars[0] = None
            else:
                self.result.append('    ' + self._stackvar(0) + ', ' + self._stackvar(1) + ' = ' + self._stackval(1) + ', ' + self._stackval(0))
                self.xvars[-1] = None
                self.xvars[-2] = None
        elif rep == ' \n\n': # Discard
            if len(self.xvars) == 0:
                self.result.append('    stack.pop()')
            else:
                self.xvars.pop()
        elif rep == ' \t\n': # Slide
            self._dumpxs()
            self.result.append('    del stack[-' + str(stmt.param.value + 1) + ':-1]')
        elif rep.startswith('\t '): # Arithmetic
            if len(self.xvars) == 0:
                self.result.append('    x0 = stack.pop()')
                self.result.append('    stack[-1] ' + _arithmap[rep] + '= x0')
            elif len(self.xvars) == 1:
                self.result.append('    stack[-1] ' + _arithmap[rep] + '= ' + self._stackval(0))
                self.xvars.pop()
            elif self.xvars[-2] is None:
                self.result.append('    ' + self._stackvar(1) + ' ' + _arithmap[rep] + '= ' + self._stackval(0))
                self.xvars.pop()
            elif self.xvars[-1] is None:
                self.result.append('    ' + self._stackvar(1) + ' = ' + self._stackval(1) + _arithmap[rep] + ' ' + self._stackval(0))
                self.xvars[-2] = None
                self.xvars.pop()
            else:
                self.xvars[-2] = '(' + self.xvars[-2] + ' ' + _arithmap[rep] + ' ' + self.xvars[-1] + ')'
                self.xvars.pop()
        elif rep == '\t\t ': # Store
            if self.checkheap:
                for i in len(self.xvars):
                    if self.xvars[i] is not None and 'heap' in self.xvars[i]:
                        self.result.append('    x' + str(i) + ' = ' + self.xvars[i])
                        self.xvars[i] = None
                self.checkheap = False
            if len(self.xvars) == 0:
                self.result.append('    x0 = stack.pop()')
                self.result.append('    heap[stack.pop()] = x0')
            elif len(self.xvars) == 1:
                self.result.append('    heap[stack.pop()] = ' + self._stackval(0))
                self.xvars.pop()
            else:
                self.result.append('    heap[' + self._stackval(1) + '] = ' + self._stackval(0))
                self.xvars.pop()
                self.xvars.pop()
        elif rep == '\t\t\t': # Retrieve
            if len(self.xvars) == 0:
                self.result.append('    stack[-1] = heap[stack[-1]]')
            else:
                self.xvars[-1] = 'heap[' + self._stackval(0) + ']'
                self.checkheap = True
        elif rep == '\n  ': # Label
            self._dumpxs()
            self.result.append('    return ' + stmt.param.name())
            self.result.append('def ' + stmt.param.name() + '():')
            self.needpass = True
        elif rep == '\n \t': # Call
            self._dumpxs()
            self.result.append('    run(' + stmt.param.name() + ')')
        elif rep == '\n \n': # Jump
            self._dumpxs()
            self.result.append('    return ' + stmt.param.name())
            self.reachable = False
        elif rep == '\n\t ': # JumpZero
            if len(self.xvars) >= 1:
                self.result.append('    if ' + self._stackval(0) + ' == 0:')
                self.xvars.pop()
                self._dumpxs2()
            else:
                self.result.append('    if stack.pop() == 0:')
            self.result.append('        return ' + stmt.param.name())
        elif rep == '\n\t\t': # JumpNegative
            if len(self.xvars) >= 1:
                self.result.append('    if ' + self._stackval(0) + ' < 0:')
                self.xvars.pop()
                self._dumpxs2()
            else:
                self.result.append('    if stack.pop() < 0:')
            self.result.append('        return ' + stmt.param.name())
        elif rep == '\n\t\n': # Return
            self._dumpxs()
            self.reachable = False
        elif rep == '\n\n\n': # End
            self.result.append('    sys.exit()')
            self.reachable = False
        elif rep == '\t\n  ': # OutputChar
            if len(self.xvars) >= 1:
                self.result.append('    sys.stdout.write(chr(' + self._stackval(0) + '))')
                self.xvars.pop()
            else:
                self.result.append('    sys.stdout.write(chr(stack.pop()))')
        elif rep == '\t\n \t': # OutputNum
            if len(self.xvars) >= 1:
                self.result.append('    sys.stdout.write(str(' + self._stackval(0) + '))')
                self.xvars.pop()
            else:
                self.result.append('    sys.stdout.write(str(stack.pop()))')
        elif rep == '\t\n\t ': # ReadChar
            self.result.append('    sys.stdout.flush()')
            self.result.append('    try:')
            self.result.append('        x' + str(len(self.xvars)) + ' = ord(sys.stdin.read(1))')
            self.result.append('    except EOFError:')
            self.result.append('        x' + str(len(self.xvars)) + ' = -1')
            if len(self.xvars) >= 1:
                self.result.append('    heap[' + self._stackval(0) + '] = x' + str(len(self.xvars)))
                self.xvars.pop()
            else:
                self.result.append('    heap[stack.pop()] = x0')
        elif rep == '\t\n\t\t': # ReadNum
            self.result.append('    sys.stdout.flush()')
            if len(self.xvars) >= 1:
                self.result.append('    heap[' + self._stackval(0) + '] = int(sys.stdin.readline())')
                self.xvars.pop()
            else:
                self.result.append('    heap[stack.pop()] = int(sys.stdin.readline())')
    
    def finish(self):
        if self.reachable:
            self.result.append('    raise IndexError')
        self.result.extend((
            'run(start)',
            'raise IndexError',
            ))

def optimise(program):
    result = _optimiser()
    for stmt in program:
        result.addstatement(stmt)
    result.finish()
    
    return '\n'.join(result.result)
