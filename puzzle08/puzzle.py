import math
import os

path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path, "input")) as file:
    lines = file.readlines()

data = lines[0]

grid = [None] * 150

least0s = 150
for layer in range(0, 15000, 150):
    val = data[layer:layer+150]
    print("Layer", layer / 150, val)
    for i in range(len(val)):
        if val[i] != '2' and not grid[i]:
            if val[i] == '0':
                grid[i] = '.'
            else:
                grid[i] = '#'

    zeros = val.count("0")
    if zeros < least0s:
        print ("Found", zeros, "0's")
        least0s = zeros
        bestLayer = val

ones = bestLayer.count("1")
twos = bestLayer.count("2")

print("Part 1:", ones * twos)

print("Part 2:")
for y in range(0,150,25):
    print ''.join(grid[y:y+25])

