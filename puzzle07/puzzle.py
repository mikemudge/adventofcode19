import math
import os
import itertools

class Computer:
    def __init__(self, data):
        self.data = data
        self.index = 0
        self.complete = False

    def readMode(self, mode, idx):
        if mode == 1:
            # Immediate mode.
            return self.data[idx]
        elif mode == 0:
            # Position mode.
            return self.data[self.data[idx]]
        else:
            raise Exception("Unknown mode")

    def runComputer(self, inputs, verbose=False):
        outputs = []
        while not self.complete:
            o = self.runComputerUntilOutput(inputs, verbose=verbose);
            outputs.append(o)
        return outputs

    def runComputerUntilOutput(self, inputs, verbose=False):
        while self.data[self.index] != 99:
            opcode = self.data[self.index]

            op = opcode % 100
            mode1 = opcode / 100 % 10
            mode2 = opcode / 1000 % 10
            mode3 = opcode / 10000 % 10

            if op == 1:
                a = self.readMode(mode1, self.index + 1)
                b = self.readMode(mode2, self.index + 2)
                c = self.data[self.index + 3]
                if verbose:
                    print("self.data[", c, "]=", a, "+", b)
                self.data[c] = a + b
                self.index += 4
            elif op == 2:
                a = self.readMode(mode1, self.index + 1)
                b = self.readMode(mode2, self.index + 2)
                c = self.data[self.index + 3]
                if verbose:
                    print("self.data[", c, "]=", a, "*", b)
                self.data[c] = a * b
                self.index += 4
            elif op == 3:
                a = self.data[self.index + 1]
                value = inputs.pop()
                if verbose:
                    print("self.data[", a, "] read input ", value)
                self.data[a] = value
                self.index += 2
            elif op == 4:
                a = self.readMode(mode1, self.index + 1)
                if verbose:
                    print("out", a)
                self.index += 2
                self.complete = self.data[self.index] == 99
                return a
            elif op == 5:
                a = self.readMode(mode1, self.index + 1)
                if a != 0:
                    b = self.readMode(mode2, self.index + 2)
                    if verbose:
                        print(a, "!=", 0, "jumpto", self.data[self.index + 2], mode2, b)
                    self.index = b
                else:
                    self.index += 3
                    if verbose:
                        print(a, "!=", 0, "false")
            elif op == 6:
                a = self.readMode(mode1, self.index + 1)
                if a == 0:
                    b = self.readMode(mode2, self.index + 2)
                    self.index = b
                    if verbose:
                        print(a, "==", 0, "jumpto", self.index)
                else:
                    self.index += 3
                    if verbose:
                        print(a, "==", 0, "false")
            elif op == 7:
                a = self.readMode(mode1, self.index + 1)
                b = self.readMode(mode2, self.index + 2)
                c = self.data[self.index + 3]
                if verbose:
                    print("self.data[", c, ']=', a, "<", b, a < b)
                if a < b:
                    self.data[c] = 1
                else:
                    self.data[c] = 0
                self.index += 4
            elif op == 8:
                a = self.readMode(mode1, self.index + 1)
                b = self.readMode(mode2, self.index + 2)
                c = self.data[self.index + 3]
                if verbose:
                    print(c, '=', a, "==", b, a == b)
                if a == b:
                    self.data[c] = 1
                else:
                    self.data[c] = 0
                self.index += 4
            else:
                raise Exception("Unknown op %d in %d" % (op, opcode))

        self.complete = True

path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path, "input")) as file:
    lines = file.readlines()

data = lines[0].split(",")
data = list(map(int, data))
print("program with", len(data), "slots")

maxSoFar = 0
for permutation in list(itertools.permutations([0, 1, 2, 3, 4])):
    outputs = [0]
    print("Attempt", permutation)
    for i in range(len(permutation)):
        # Inputs are read from right to left using pop.
        inputs = [outputs[0], permutation[i]]
        print("inputs", inputs)
        c = Computer(data[:])
        outputs = c.runComputer(inputs, verbose=True)
        print("finished with", outputs[0])

    if outputs[0] > maxSoFar:
        maxSoFar = outputs[0]

    print("Result", outputs)

print("Part 1:", maxSoFar)

maxSoFar = 0
for permutation in list(itertools.permutations([5, 6, 7, 8, 9])):
    print("Attempt", permutation)
    computers = []
    output = 0
    for i in range(len(permutation)):
        c = Computer(data[:])
        computers.append(c)
        inputs = [output, permutation[i]]
        output = c.runComputerUntilOutput(inputs)

    i = 5
    while not computers[4].complete:
        inputs = [output]
        c = computers[i % 5]
        i += 1
        output = c.runComputerUntilOutput(inputs)

    if output > maxSoFar:
        maxSoFar = output

    print("Result", i, output)

print("Part 2:", maxSoFar)
