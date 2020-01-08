import math
import os
import itertools
import sys
import time

from Queue import Queue

class Computer:
    def __init__(self, data):
        self.data = data
        self.index = 0
        self.complete = False
        self.relative_base = 0

    def readMode(self, mode, idx):
        if mode == 2:
            # Relative mode.
            return self.data[self.relative_base + self.data[idx]]
        elif mode == 1:
            # Immediate mode.
            return self.data[idx]
        elif mode == 0:
            # Position mode.
            pos = self.data[idx]
            size = pos + 1 - len(self.data)
            if size > 0:
                print("Growing memory to fit", pos)
                # Grow the memory to fit everything.
                self.data.extend([0] * size)
            return self.data[pos]
        else:
            raise Exception("Unknown mode")

    def saveMode(self, mode, idx, value, verbose=False):
        if mode == 1:
            raise Exception("Immediate mode not supported for write")
        elif mode == 2:
            if verbose:
                print("self.data[", self.relative_base + idx, "]=", value)
            self.data[self.relative_base + idx] = value
        elif mode == 0:
            if verbose:
                print("self.data[", idx, "]=", value)
            self.data[idx] = value
        else:
            raise Exception("Unknown mode")

    def runComputer(self, inputs, verbose=False):
        outputs = []
        while not self.complete:
            o = self.runComputerUntilOutput(inputs, verbose=verbose)
            if o is not None:
                outputs.append(o)
        return outputs

    def runComputerUntilOutput(self, inputs, verbose=False):
        while self.data[self.index] != 99:
            opcode = self.data[self.index]

            op = opcode % 100
            mode1 = opcode / 100 % 10
            mode2 = opcode / 1000 % 10
            mode3 = opcode / 10000 % 10

            if verbose:
                print(self.index, "op", opcode)

            if op == 1:
                a = self.readMode(mode1, self.index + 1)
                b = self.readMode(mode2, self.index + 2)
                c = self.data[self.index + 3]
                self.saveMode(mode3, c, a + b, verbose)
                self.index += 4
            elif op == 2:
                a = self.readMode(mode1, self.index + 1)
                b = self.readMode(mode2, self.index + 2)
                c = self.data[self.index + 3]
                if verbose:
                    print("self.data[", c, "]=", a * b, a, "*", b)
                self.saveMode(mode3, c, a * b)
                self.index += 4
            elif op == 3:
                a = self.data[self.index + 1]
                value = inputs.pop()
                if verbose:
                    print("self.data[", a, "] read input ", value)
                self.saveMode(mode1, a, value)
                self.index += 2
            elif op == 4:
                a = self.readMode(mode1, self.index + 1)
                if verbose:
                    print("out", a)
                self.index += 2
                self.complete = self.data[self.index] == 99
                return a
            elif op == 5:
                # Jump if not equal to 0.
                a = self.readMode(mode1, self.index + 1)
                if a != 0:
                    b = self.readMode(mode2, self.index + 2)
                    if verbose:
                        print(a, "!=", 0, "jumpto", self.data[self.index + 2], mode2, b)
                    self.index = b
                else:
                    self.index += 3
                    if verbose:
                        print(a, "is", 0, "no-op")
            elif op == 6:
                # Jump if equals 0
                a = self.readMode(mode1, self.index + 1)
                if a == 0:
                    b = self.readMode(mode2, self.index + 2)
                    self.index = b
                    if verbose:
                        print(a, "==", 0, "jumpto", self.index)
                else:
                    self.index += 3
                    if verbose:
                        print(a, "is not", 0, "no-op")
            elif op == 7:
                a = self.readMode(mode1, self.index + 1)
                b = self.readMode(mode2, self.index + 2)
                c = self.data[self.index + 3]
                if verbose:
                    print("self.data[", c, ']=', int(a < b), "because", a, "<", b)
                if a < b:
                    self.saveMode(mode3, c, 1)
                else:
                    self.saveMode(mode3, c, 0)
                self.index += 4
            elif op == 8:
                a = self.readMode(mode1, self.index + 1)
                b = self.readMode(mode2, self.index + 2)
                c = self.data[self.index + 3]
                if verbose:
                    print(c, '=', a, "==", b, a == b)
                if a == b:
                    self.saveMode(mode3, c, 1)
                else:
                    self.saveMode(mode3, c, 0)
                self.index += 4
            elif op == 9:
                a = self.readMode(mode1, self.index + 1)
                if verbose:
                    print ("rel", self.relative_base, "+=", a)
                self.relative_base += a
                self.index += 2
            else:
                raise Exception("Unknown op %d in %d" % (op, opcode))

        self.complete = True

def printBoard(visited):
    for y in range(40):
        v = ""
        if y in visited:
            v = range(50)
            for i in v:
                v[i] = " "
                x = i
                if x in visited[y]:
                    v[i] = str(unichr(visited[y][x]))
                    # if visited[y][x] == 35:
                    #     v[i] = "."
                    # if visited[y][x] == 46:
                    #     v[i] = "#"
        print ''.join(v)

path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path, "input")) as file:
    lines = file.readlines()

data = lines[0].split(",")
data = list(map(int, data))
print("program with", len(data), "slots")

inputs = []
visited = {}
c = Computer(data[:])
c.data.extend([0] * 10000)

x = 0
y = 0
while not c.complete:
    o = c.runComputerUntilOutput(inputs)
    if o == 10:
        y += 1
        x = 0
        continue
    if y not in visited:
        visited[y] = {}

    visited[y][x] = o
    x += 1

printBoard(visited)

# TODO find intersections.

s = 0
for y in visited:
    if y - 1 not in visited:
        continue
    if y + 1 not in visited:
        continue
    for x in visited[y]:
        if x - 1 not in visited[y]:
            continue
        if x + 1 not in visited[y]:
            continue
        # If this spot or any of its neighbours are .'s then we are not on an intersection.
        if visited[y][x] == 46:
            continue
        if visited[y][x - 1] == 46 or visited[y][x + 1] == 46:
            continue
        if visited[y - 1][x] == 46 or visited[y + 1][x] == 46:
            continue
        print("intersection at", x, y)
        s += y * x

# 5538 was too high, included . surrounded by #'s
print("Part 1:", s)

inputs = list('A,B,A,C,B,A,C,B,A,C\n') \
    + list('L,12,L,12,L,6,L,6\n') \
    + list('R,8,R,4,L,12\n') \
    + list('L,12,L,6,R,12,R,8\n') \
    + list('n\n')

'''
L12L12L6L6 A
R8R4L12    B
L12L12L6L6 A
L12L6R12R8 C
R8R4L12    B
L12L12L6L6 A
L12L6R12R8 C
R8R4L12    B
L12L12L6L6 A
L12L6R12R8 C
'''

inputs = list(reversed(map(ord, inputs)))
print(inputs)

c = Computer(data[:])
# Wake up the robot
c.data.extend([0] * 10000)
c.data[0] = 2

x = 0
y = 0
visited = {}

while not c.complete:
    line = ""
    o = c.runComputerUntilOutput(inputs)
    if c.complete:
        break
    while o != 10:
        line += unichr(o)
        o = c.runComputerUntilOutput(inputs)
    print line

# while not c.complete:
#     o = c.runComputerUntilOutput(inputs)
#     if o == 10:
#         y += 1
#         x = 0
#         continue

#     if o != 35 and o != 46:
#         print("o", o, unichr(o))
#         error += unichr(o)

#     if y not in visited:
#         visited[y] = {}

#     visited[y][x] = o
#     x += 1

# printBoard(visited)
print(o)

print("Part 2:", o)
