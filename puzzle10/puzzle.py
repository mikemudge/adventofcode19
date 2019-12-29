import math
import os
import itertools

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path, "input")) as file:
    lines = file.readlines()

satellites = []
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == "#":
            satellites.append(Point(x, y))

print("Num satellites", len(satellites))

numSatellites = 0
# Find satellite which can see the most satellites.
for s in satellites:
    visited = {}
    seen = 0
    for s2 in satellites:
        if s == s2:
            continue
        dx = s2.x - s.x
        dy = s2.y - s.y
        # Can see?
        # m = dy / dx
        # print(m)
        ang = math.atan2(dy, dx)
        if not ang in visited:
            seen += 1
            visited[ang] = s2
    if seen > numSatellites:
        best = s
        numSatellites = seen

print("Part 1:", numSatellites)
print("Best is at ", best.x, best.y)

radialSats = {}
for s in satellites:
    if s == best:
        # Skip yourself
        continue
    dx = s.x - best.x
    dy = s.y - best.y
    ang = math.atan2(dy, dx)
    # We want to start at "up" which is 1/0
    if ang < math.atan2(-1, 0):
        ang += math.pi * 2
    if not ang in radialSats:
        radialSats[ang] = [s]
    else:
        radialSats[ang].append(s)

ordered = sorted(radialSats)
for i, x in enumerate(ordered):
    # The list at index x is not sorted, so this isn't always correct.
    # Its fine when len() = 1
    print("The", i, "asteroid to be vaporized is at", radialSats[x][0].x, radialSats[x][0].y, len(radialSats[x]), x)

k = ordered[199]
print(k, radialSats[k])
print(k, radialSats[k][0].x, radialSats[k][0].y)

# 1900 is too high.
# 1805 was too high.
# 19 is wrong.
# 1604 is wrong.
print("Part 2:", radialSats[k][0].x * 100 + radialSats[k][0].y)

print(math.atan2(-1, 0))
print(math.atan2(-1, 1))
