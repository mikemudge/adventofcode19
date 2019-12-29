import math
import os
import itertools

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

inputs = [1]
c = Computer(data[:])
c.data.extend([0] * 100)
d = 0
x = 0
y = 0
visited = {}
while not c.complete:
    key = str(x) + ":" + str(y)
    color = 0
    if key in visited:
        color = visited[key]

    print(x, y, key, d, color)
    inputs = [color]
    paint = c.runComputerUntilOutput(inputs)
    direction = c.runComputerUntilOutput(inputs)
    visited[key] = paint

    if direction == 1:
        d = (d + 1) % 4
    else:
        d = (d + 3) % 4
    if d == 0:
        y -= 1
    elif d == 1:
        x += 1
    elif d == 2:
        y += 1
    elif d == 3:
        x -= 1

print("Part 1:", len(visited))

c = Computer(data[:])
c.data.extend([0] * 1000)
d = 0
x = 0
y = 0
visited = {
    0: {
        0: 1
    }
}

print("Part 2:")
while not c.complete:
    if y not in visited:
        print("Making a y =", y)
        visited[y] = {}

    color = 0
    if x in visited[y]:
        color = visited[y][x]

    print(x, y, d, color)
    inputs = [color]
    paint = c.runComputerUntilOutput(inputs)
    direction = c.runComputerUntilOutput(inputs)
    if c.complete:
        break

    visited[y][x] = paint

    if direction == 1:
        d = (d + 1) % 4
    elif direction == 0:
        d = (d + 3) % 4
    else:
        raise Exception("Bad direction", paint, direction)

    if d == 0:
        y -= 1
    elif d == 1:
        x += 1
    elif d == 2:
        y += 1
    elif d == 3:
        x -= 1

for y in visited:
    v = range(50)
    for x in range(50):
        v[x] = "."
        if x in visited[y]:
            # print(visited[y][x])
            if visited[y][x] == 1:
                v[x] = "#"
    print ''.join(v)
