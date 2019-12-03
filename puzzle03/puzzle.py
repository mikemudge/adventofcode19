import math
import os
import numpy as np

path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path, "input")) as file:
    lines = file.readlines()
    wire1 = lines[0]
    wire2 = lines[1]

# wire1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
# wire2 = "U62,R66,U55,R34,D71,R55,D58,R83"
# 159, 610
# wire1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
# wire2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
# 135, 410

x = 0
y = 0
points = [(x, y, 0)]
steps = 0
for move in wire1.split(","):
    dis = int(move[1:])
    print(move[0], dis)
    if move[0] == 'U':
        y -= dis
    if move[0] == 'D':
        y += dis
    if move[0] == 'L':
        x -= dis
    if move[0] == 'R':
        x += dis
    steps += dis
    points.append((x, y, steps))

print(points)

print("wire 2")

x = 0
y = 0
best = [1000, 1000]
best2 = 4000000000
steps = 0
for move in wire2.split(","):
    dis = int(move[1:])
    print(move[0], dis)
    bx = x
    by = y
    if move[0] == 'U':
        y -= dis
    if move[0] == 'D':
        y += dis
    if move[0] == 'L':
        x -= dis
    if move[0] == 'R':
        x += dis
    if bx == x:
        ly = min(by, y)
        hy = max(by, y)
        for i in range(len(points) - 1):
            p = points[i]
            np = points[i + 1]
            if p[0] == np[0]:
                # 2 vertical lines won't cross
                continue
            py = p[1]
            lx = min(p[0], np[0])
            hx = max(p[0], np[0])
            if x >= lx and x <= hx and py >= ly and py <= hy:
                if abs(x) + abs(py) == 0:
                    continue
                print(p, np, 'crosses', bx, by, x, y, 'at', x, py)
                if abs(x) + abs(py) < best[0] + best[1]:
                    best = (abs(x), abs(py))

                # Part 2
                totSteps = p[2] + abs(py - by) + steps + abs(p[0] - x)
                if totSteps < best2:
                    best2 = totSteps
    elif by == y:
        lx = min(bx, x)
        hx = max(bx, x)
        for i in range(len(points) - 1):
            p = points[i]
            np = points[i + 1]
            if p[1] == np[1]:
                # 2 horizontal lines won't cross
                continue
            px = p[0]
            ly = min(p[1], np[1])
            hy = max(p[1], np[1])
            if px >= lx and px <= hx and y >= ly and y <= hy:
                if abs(px) + abs(y) == 0:
                    continue
                print(p, np, 'crosses', bx, by, x, y, 'at', px, y)
                if abs(px) + abs(y) < best[0] + best[1]:
                    best = (abs(px), abs(y))

                # Part 2
                totSteps = p[2] + abs(y - p[1]) + steps + abs(px - bx)
                if totSteps < best2:
                    best2 = totSteps
    steps += dis

print("Part 1:", best, sum(best))

print("Part 2:", best2)
