import math
import os
import itertools

class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def updateV(self, m):
        if self.x < m.x:
            self.vx += 1
        if self.x > m.x:
            self.vx -= 1
        if self.y < m.y:
            self.vy += 1
        if self.y > m.y:
            self.vy -= 1
        if self.z < m.z:
            self.vz += 1
        if self.z > m.z:
            self.vz -= 1

    def updateP(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def energy(self):
        pot = abs(self.x) + abs(self.y) + abs(self.z)
        kin = abs(self.vx) + abs(self.vy) + abs(self.vz)
        return pot * kin

io = Moon(x=-14, y=-4, z=-11)
europa = Moon(x=-9, y=6, z=-7)
ganymede = Moon(x=4, y=1, z=4)
callisto = Moon(x=2, y=-14, z=-9)
moons = [io, europa, ganymede, callisto]

# Sample
# io = Moon(x=-8, y=-10, z=0)
# europa = Moon(x=5, y=5, z=10)
# ganymede = Moon(x=2, y=-7, z=3)
# callisto = Moon(x=9, y=-8, z=-3)
# moons = [io, europa, ganymede, callisto]

xvisited = {}
yvisited = {}
zvisited = {}
xcycled = False
ycycled = False
zcycled = False

for i in range(1000000):
    if not xcycled:
        xstates = "%d:%d:%d:%d:%d:%d:%d:%d" % (io.x,europa.x,ganymede.x,callisto.x,
            io.vx,europa.vx,ganymede.vx,callisto.vx)

        if xstates in xvisited:
            print("X repeats at", xvisited[xstates], i)
            # 0, 186028
            xcycled = True
        else:
            xvisited[xstates] = i

    if not ycycled:
        ystates = "%d:%d:%d:%d:%d:%d:%d:%d" % (io.y,europa.y,ganymede.y,callisto.y,
            io.vy,europa.vy,ganymede.vy,callisto.vy)

        if ystates in yvisited:
            print("Y repeats at", yvisited[ystates], i)
            # 0, 161428
            ycycled = True
        else:
            yvisited[ystates] = i

    if not zcycled:
        zstates = "%d:%d:%d:%d:%d:%d:%d:%d" % (io.z,europa.z,ganymede.z,callisto.z,
            io.vz,europa.vz,ganymede.vz,callisto.vz)

        if zstates in zvisited:
            print("Z repeats at", zvisited[zstates], i)
            # 0, 167624
            zcycled = True
        else:
            zvisited[zstates] = i

    if xcycled and ycycled and zcycled:
        break

    # Update velocity
    for m in moons:
        for m2 in moons:
            if m == m2:
                continue
            m.updateV(m2)

    # Update position
    for m in moons:
        m.updateP()

    if i == 999:
        # This is 1000 steps.
        energy = sum([m.energy() for m in moons])
        # 543 is too low.
        print("Part 1:", energy)

for m in moons:
    print(m.x,m.y,m.z,m.vx,m.vy,m.vz)



# 0, 186028
# 2, 2, 46507

# 0, 161428
# 2, 2, 40357

# 0, 167624
# 2, 2, 2, 23, 911

result = 167624 * 40357 * 46507
print(result)
