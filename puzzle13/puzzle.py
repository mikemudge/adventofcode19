import math
import os
import itertools
import sys
import time

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
    for y in visited:
        v = range(40)
        for x in v:
            v[x] = "."
            if x in visited[y]:
                if visited[y][x] == 1:
                    v[x] = "#"
                if visited[y][x] == 2:
                    v[x] = "-"
                if visited[y][x] == 3:
                    v[x] = "_"
                if visited[y][x] == 4:
                    v[x] = "o"
        print ''.join(v)

path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path, "input")) as file:
    lines = file.readlines()

# Samples
# lines = ["109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"]
# lines = ["1102,34915192,34915192,7,4,7,99,0"]
# lines = ["104,1125899906842624,99"]

data = lines[0].split(",")
data = list(map(int, data))
print("program with", len(data), "slots")

inputs = []
visited = {}
c = Computer(data[:])
c.data.extend([0] * 1000)

while not c.complete:
    x = c.runComputerUntilOutput(inputs)
    y = c.runComputerUntilOutput(inputs)
    t = c.runComputerUntilOutput(inputs)
    if c.complete:
        break

    if y not in visited:
        visited[y] = {}

    visited[y][x] = t

counts = [0, 0, 0, 0, 0, 0]
for y in visited:
    for x in visited[y]:
        counts[visited[y][x]] += 1

print("Part 1:", counts[2])

printBoard(visited)

print("Part 2:")
data2 = data[:]
# Add 2 quarters for part 2.
data2[0] = 2
visited = {}
c = Computer(data2)
c.data.extend([0] * 1000)

slow = 'slow' in sys.argv
score = 0
px = 0
bx = 0
timer = 0
inputs = [0, 0] + [1] * 100
while not c.complete:
    if px < bx:
        inputs = [1]
    elif px > bx:
        inputs = [-1]
    else:
        inputs = [0]
    x = c.runComputerUntilOutput(inputs)
    y = c.runComputerUntilOutput(inputs)
    t = c.runComputerUntilOutput(inputs)
    if c.complete:
        break

    if slow:
        print("Current score:", score)
        printBoard(visited)
        timer+=1
        if timer > 40 * 24:
            time.sleep(0.1)
    if x == -1 and y == 0:
        score = t
        continue

    # You can see the ball moving (unset/set) here.
    # print("Change", x, y, t)
    if t == 4:
        # Ball location
        bx = x
    if t == 3:
        # paddle location
        px = x

    if y not in visited:
        visited[y] = {}

    visited[y][x] = t

printBoard(visited)
print("Final score:", score)
