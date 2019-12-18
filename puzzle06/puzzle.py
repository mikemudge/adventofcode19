import os

path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path, "input")) as file:
    lines = [line.rstrip() for line in file]

class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []

    def countOrbits(self, depth):
        # Orbits for this node is the depth.
        sumDepths = depth
        # Then ask the children for their orbit counts.
        for child in self.children:
            sumDepths += child.countOrbits(depth + 1)
        return sumDepths

data = {}
for line in lines:
    a, b = line.split(")")
    print("line", a, b)
    # a is orbitted by b
    if a not in data:
        data[a] = Node(a)
    if b not in data:
        data[b] = Node(b)

    data[b].parent = data[a]
    data[a].children.append(data[b])

# Who is the root?
node = data.values()[0]
while node.parent:
    node = node.parent

print("Root node", node.name)

print("Part 1:", node.countOrbits(0))

sanList =[]
node = data["SAN"]
while node.parent:
    node = node.parent
    sanList.append(node.name)

youList =[]
node = data["YOU"]
while node.parent:
    node = node.parent
    youList.append(node.name)

sanLen = len(sanList)
youLen = len(youList)
print("SAN", sanLen)
print("YOU", youLen)
for i in range(len(sanList)):
    print(i, sanList[sanLen - i - 1], youList[youLen - i - 1])
    if sanList[sanLen - i - 1] != youList[youLen - i - 1]:
        break

print("SAN", sanList[0], sanList[sanLen - i - 1], sanList[sanLen - i])
print("YOU", youList[0], youList[youLen - i - 1], youList[youLen - i])
print("i", i)
commonLen = i

# 5 - 4 + 7 - 4 = 4
transfers = sanLen - commonLen + youLen - commonLen

print("Part 2:", transfers)
