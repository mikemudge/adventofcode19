import math
import os

path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path, "input")) as file:
    lines = file.readlines()
    sum = 0
    sum2 = 0
    for i, line in enumerate(lines):
        print(i, ' has ', line[:-1])
        fuel = math.floor(int(line) / 3) - 2
        sum += fuel

        sum2 += fuel

        weight = fuel
        while True:
            extrafuel = math.floor(weight / 3) - 2
            if extrafuel >= 0:
                sum2 += extrafuel
            else:
                break
            weight = extrafuel

print("Part 1:", sum)

# 5219097 was too high.
# 5216273
print("Part 2:", sum2)
