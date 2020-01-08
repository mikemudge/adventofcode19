import math
import os
import itertools
import sys
import time

path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path, "input")) as file:
    lines = file.readlines()

data = list(lines[0])

# Sample
# data = list("12345678")

data = map(int, data)

print("numbers", len(data))

def pattern(outputIndex, patternIndex):
    p = [0,1,0,-1]
    # The pattern repeats the output index times (outputIndex + 1)
    # It starts at index 1 (+1), and repeats infinitely as needed (% 4)
    index = int((patternIndex + 1) / (outputIndex + 1)) % 4
    return p[index]

# for i in range(len(data)):
#     patternValues = [str(pattern(i, ii)) for ii in range(8)]
#     print(i, ','.join(patternValues))

# for iter in range(100):
#     output = []
#     for i,v in enumerate(data):
#         s = 0
#         # pattern is 0's until i so we can skip those.
#         for ii in range(i, len(data)):
#             s += data[ii] * pattern(i, ii)
#         output.append(abs(s) % 10)
#         # print(s, output[i])
#     # print(''.join(map(str,output)))
#     data = output

# print("Part 1:", ''.join(map(str,output[:8])))

# Part 2 is 10000x the input, so will need an optimized approach.
# input is already 650 long, so 6.5M is quite large.
# we are only interested in the chars after 5,971,989 so this would reduce it to ~600K
# all would be 1's after that as well? so could optimize reusage.
# print("Part 2:", maxd)

startIndex = 5971989 % 650
rest = len(data) * 10000 - 5971989
print(rest, startIndex)
# (528011, 439)
longdata = data * (528011 / 650 + 1)
longdata = longdata[439:]
print(len(longdata))
data = longdata

for iter in range(100):
    output = []
    print(iter, len(data), data[rest - 2], data[rest - 1])
    s = 0
    for i,v in enumerate(data):
        s += data[rest - i - 1]
        output.append(abs(s) % 10)
    data = list(reversed(output))

# 77045669 is too high
print("Part 2:", ''.join(map(str,data[:8])))


