import math
import os
import itertools
import sys
import time

class Node:
    def __init__(self, name, makes):
        self.name = name
        self.makes = makes
        self.children = []

    def create(self, num, nodes):
        if self.name == "ORE":
            return num

        print("Making", num, self.name)
        oreSum = 0
        for c in self.children:
            name = c[1]
            oreSum += num * nodes[name].create(c[0], nodes)
        return oreSum

path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path, "input")) as file:
    lines = file.readlines()

nodes = {
    "ORE": Node("ORE", 0)
}
for line in lines:
    line = line.rstrip()
    (i, o) = line.split(" => ")

    (num, chem) = o.split(" ")

    print(chem)
    node = Node(chem, int(num))
    nodes[chem] = node

    parts = i.split(", ")
    for p in parts:
        (num, name) = p.split(" ")
        num = int(num)
        node.children.append([num, name])

print("Part 1:", nodes['FUEL'].create(1, nodes))

order = ["ORE"]
ordered = {"ORE": True}
while len(order) < len(nodes):
    for node in nodes:
        if node in ordered:
            continue
        makable = True
        for c in nodes[node].children:
            name = c[1]
            if name not in ordered:
                makable = False
        if makable:
            print("Adding ", node)
            order.append(node)
            ordered[node] = True

def oreRequired(needs, nodes, order):
    for chem in reversed(order):
        if chem == "ORE":
            continue
        # Remove this item from needs.
        howmany = needs.pop(chem)
        node = nodes[chem]
        batches = int(math.ceil(1.0 * howmany / node.makes))
        # print("Making", howmany, chem, "in", batches, "batches of", node.makes)

        for c in node.children:
            x = c[1]
            if x not in needs:
                needs[x] = 0
            needs[x] += c[0] * batches
    return needs["ORE"]

needs = {
    "FUEL": 1
}
oreNeeded = oreRequired(needs, nodes, order)

print("Part 1:", oreNeeded)

# 1000000000000 / 741927 = 1347841
# How much fuel can we make with 1 Trillion ORE? At least 1347841 because we know we can make 1 FUEL with 741927 ORE
attempt = 1000000000000 / 741927
x = 0
attempt += 1000000
# TODO binary search could be quicker here.
# Manually picking a start point worked pretty fast though.
while x < 1000000000000:
    needs = {
        "FUEL": attempt
    }
    x = oreRequired(needs, nodes, order)
    print(attempt, x)
    attempt += 1
