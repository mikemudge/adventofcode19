import math
import os

path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path, "input")) as file:
    lines = file.readlines()

data = lines[0].split(",")
data = list(map(int, data))

index = 0

print(len(data))

# Part one changes.
data[1] = 42
data[2] = 59

while data[index] != 99:
    print(index, data[index])
    a = data[index + 1]
    b = data[index + 2]
    c = data[index + 3]
    if data[index] == 1:
        # Sum
        data[c] = data[a] + data[b]
    elif data[index] == 2:
        # Multiply
        data[c] = data[a] * data[b]
    index += 4

# Valid only when 12, 2 are used for inputs.
print("Part 1:", data[0])


# 1000 = 4945061
# 1100 = 5405861
print(5405861 - 4945061)
# 460800

print((19690720 - 4945061) / 460800)
# 1200 = 5866662
# 1201 = 5866662
# 1202 = 5866663
# 1299 = 5866760
# 4200 = 19690661
# 4259 = 19690720
print(19690720 - 19690661)

print("Part 2:", data)

# Need to find initial values for 1, 2 for this.
# Want value at 0 to be 19690720
