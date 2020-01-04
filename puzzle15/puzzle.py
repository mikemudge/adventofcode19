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
    for y in range(-22,20):
        v = ""
        if y in visited:
            v = range(45)
            for i in v:
                v[i] = " "
                x = i - 25
                if x in visited[y]:
                    if visited[y][x] == 1:
                        v[i] = "."
                    if visited[y][x] == 2:
                        v[i] = "#"
                    if visited[y][x] == 3:
                        v[i] = "o"
                    if visited[y][x] == 4:
                        v[i] = "?"
                    if visited[y][x] == 5:
                        v[i] = "X"
        print ''.join(v)

def printDistances(visited, distances):
    for y in range(-22,20):
        v = ""
        if y in visited:
            v = range(45)
            for i in v:
                v[i] = " "
                x = i - 25
                if x in visited[y]:
                    if visited[y][x] == 2:
                        v[i] = "#"
                if y in distances and x in distances[y]:
                    v[i] = str(distances[y][x] % 10)

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
c.data.extend([0] * 1000)

xs = [None, 0, 0, 1, -1]
ys = [None, -1, 1, 0, 0]
x = 0
y = 0
direction = 1
directions = {
    (0, 0, 0, 0): 1,
    (0, 1, 0, 0): 4,
    (0, 1, 0, 2): 1,
    (2, 1, 0, 2): 3,
    (0, 0, 0, 1): 1,
    (2, 0, 0, 1): 3,
    (2, 0, 2, 1): 2,
    (1, 0, 0, 0): 3,
    (1, 0, 2, 0): 2,
    (0, 1, 0, 2): 1,
    (0, 2, 1, 0): 4,
    (0, 2, 1, 2): 1,
    (0, 0, 1, 0): 2,
    (1, 2, 2, 0): 4,
    (1, 2, 0, 0): 3,
    (1, 2, 2, 2): 1,
    (1, 1, 2, 0): 4,
    (1, 1, 2, 2): 5,
    (2, 1, 2, 1): 6,
    (1, 2, 1, 0): 4,
    (0, 2, 0, 1): 1,
    (2, 2, 0, 1): 3,
    (0, 2, 2, 1): 1,
    (0, 1, 2, 2): 1,
    (2, 1, 2, 0): 4,
    (2, 2, 1, 0): 4,
    (2, 2, 1, 2): 3,
    (2, 2, 1, 1): 5,
    (1, 2, 2, 1): 7,
    (2, 0, 1, 1): 2,
    (1, 0, 1, 0): 2,
    (1, 2, 0, 2): 3,
    (2, 1, 2, 2): 2,
    (1, 2, 1, 2): 6,
    (0, 2, 1, 1): 1,
    (1, 2, 1, 1): 10,
    (0, 1, 1, 0): 4,
    (0, 1, 1, 2): 1,
    (2, 2, 2, 1): 4,
    (2, 1, 1, 1): 8,
    (2, 1, 1, 2): 7,
    (1, 1, 0, 2): 3,
    (1, 1, 1, 2): 11,
    (0, 1, 0, 1): 1,
    (2, 1, 0, 1): 3,
    (1, 0, 2, 2): 2,
    (0, 1, 1, 1): 1,
    (1, 0, 0, 1): 3,
    (1, 0, 2, 1): 2,
    (2, 1, 0, 0): 4,
    (2, 0, 1, 2): 2,
    (1, 0, 0, 2): 3,
    (1, 1, 2, 1): 9,
    (0, 1, 2, 0): 4,
    (0, 0, 2, 1): 1,
    (1, 0, 1, 1): 2,
}
visited[0] = {0:1}
lastdirection = 1
steps = 0
while not c.complete:
    # TODO Pick a direction?

    v = [0,0,0,0]
    if y - 1 in visited:
        if x in visited[y-1]:
            v[0] = visited[y-1][x]
    if y + 1 in visited:
        if x in visited[y+1]:
            v[1] = visited[y+1][x]

    if x - 1 in visited[y]:
        v[2] = visited[y][x-1]
    if x + 1 in visited[y]:
        v[3] = visited[y][x+1]

    key = tuple(v)
    direction = directions[key]
    if direction == 5:
        direction = lastdirection
    if direction == 6:
        # Turn one.
        if lastdirection == 1:
            direction = 4
        elif lastdirection == 2:
            direction = 3
        elif lastdirection == 3:
            direction = 2
        elif lastdirection == 4:
            direction = 1
    if direction == 7:
        # Turn one.
        if lastdirection == 1:
            direction = 3
        elif lastdirection == 2:
            direction = 4
        elif lastdirection == 3:
            direction = 1
        elif lastdirection == 4:
            direction = 2
    if direction == 8:
        # Turn one.
        if lastdirection == 1:
            direction = 4
        elif lastdirection == 3:
            direction = 3
        elif lastdirection == 4:
            direction = 2
    if direction == 9:
        # Turn one.
        if lastdirection == 1:
            direction = 4
        elif lastdirection == 2:
            direction = 2
        elif lastdirection == 3:
            direction = 1
    if direction == 10:
        # Turn one.
        if lastdirection == 2:
            direction = 3
        elif lastdirection == 3:
            direction = 1
        elif lastdirection == 4:
            direction = 4
    if direction == 11:
        # Turn one.
        if lastdirection == 1:
            direction = 1
        elif lastdirection == 2:
            direction = 3
        elif lastdirection == 4:
            direction = 2

    inputs = [direction]
    status = c.runComputerUntilOutput(inputs)

    ny = y+ys[direction]
    nx = x-xs[direction]
    # print("Moving", direction, nx, ny, status)

    if ny not in visited:
        visited[ny] = {}

    if status == 0:
        visited[ny][nx] = 2
    elif status == 1:
        lastdirection = direction
        visited[ny][nx] = 1
        x = nx
        y = ny
    elif status == 2:
        visited[ny][nx] = 1
        winx = nx
        winy = ny
        x = nx
        y = ny
        # Winner
        prev = visited[y][x]
        visited[y][x] = 3
        printBoard(visited)
        time.sleep(.1)
        visited[y][x] = prev
        # break

    if steps > 2500:
        prev = visited[y][x]
        visited[y][x] = 3
        printBoard(visited)
        time.sleep(.1)
        visited[y][x] = prev
    steps += 1

    if x == 0 and y == 0:
        # Return to start
        break

print("Winner", x, y)

visited[y][x] = 3
visited[winy][winx] = 5
printBoard(visited)

# Calculate min distance to goal using visited.
distances = {}
x = 0
y = 0
queue = Queue()
queue.put((winx, winy, 0))
i = 0
maxd = 0
while not queue.empty():
    i += 1
    (x, y, d) = queue.get()

    if y not in distances:
        distances[y] = {}

    if y in visited and x in visited[y]:
        if visited[y][x] == 2:
            # Skip walls
            continue
        # only update distance if an improvement is made.
        # As this is breadth first this shouldn't happen often,
        # only if there are 2+ paths with equal length to another location.
        if x not in distances[y] or d < distances[y][x]:
            distances[y][x] = d
            maxd = max(d, maxd)
            # Add all the next locations
            queue.put((x, y - 1, d + 1))
            queue.put((x, y + 1, d + 1))
            queue.put((x - 1, y, d + 1))
            queue.put((x + 1, y, d + 1))
    if i % 500:
        printDistances(visited, distances)

printDistances(visited, distances)

print("Part 1:", distances[0][0])
print("Part 2:", maxd)
