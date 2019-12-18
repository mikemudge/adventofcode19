import math
import os

class Param():
    def __init__(self, mode, value):
        self.data = data

def readMode(mode, data, idx):
    if (mode == 1):
        # Immediate mode.
        return data[idx]
    else:
        # Position mode.
        return data[data[idx]]

def runComputer(data, inputs):
    print(len(data))

    index = 0
    outputs = []

    while data[index] != 99:
        opcode = data[index]

        print(index, opcode)

        op = opcode % 100
        mode1 = opcode / 100 % 10
        mode2 = opcode / 1000 % 10
        mode3 = opcode / 10000 % 10

        if op == 1:
            a = readMode(mode1, data, index + 1)
            b = readMode(mode2, data, index + 2)
            c = data[index + 3]
            print(c, "=", a, "+", b, data[index + 1], data[index + 2], data[index + 3])
            data[c] = a + b
            index += 4
        elif op == 2:
            a = readMode(mode1, data, index + 1)
            b = readMode(mode2, data, index + 2)
            c = data[index + 3]
            print(c, "=", a, "*", b)
            data[c] = a * b
            index += 4
        elif op == 3:
            a = data[index + 1]
            value = inputs.pop()
            print(a, "=", value)
            data[a] = value
            index += 2
        elif op == 4:
            a = readMode(mode1, data, index + 1)
            outputs.append(a)
            print("out", a)
            index += 2
        elif op == 5:
            a = readMode(mode1, data, index + 1)
            if a != 0:
                index = readMode(mode2, data, index + 2)
            else:
                index += 3
        elif op == 6:
            a = readMode(mode1, data, index + 1)
            if a == 0:
                index = readMode(mode2, data, index + 2)
            else:
                index += 3
        elif op == 7:
            a = readMode(mode1, data, index + 1)
            b = readMode(mode2, data, index + 2)
            c = data[index + 3]
            if a < b:
                data[c] = 1
            else:
                data[c] = 0
            index += 4
        elif op == 8:
            a = readMode(mode1, data, index + 1)
            b = readMode(mode2, data, index + 2)
            c = data[index + 3]
            if a == b:
                data[c] = 1
            else:
                data[c] = 0
            index += 4
        else:
            raise Exception("Unknown op %d in %d" % (op, opcode))

    return outputs

path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path, "input")) as file:
    lines = file.readlines()

data = lines[0].split(",")
data = list(map(int, data))

inputs = [1]

outputs = runComputer(data[:], inputs)

print("Part 1:", outputs)

inputs2 = [5]
outputs = runComputer(data[:], inputs2)

print("Part 2:", outputs)
