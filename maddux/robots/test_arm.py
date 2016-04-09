from link import Link
from arm import Arm
import numpy as np
import math

L1 = Link(0,0,0,1.571)
L2 = Link(0,0,0,-1.571)
L3 = Link(0,0.4318,0,-1.571)
L4 = Link(0,0,0,1.571)
L5 = Link(0,0.4318,0,1.571)
L6 = Link(0,0,0,-1.571)
links = np.array([L1, L2, L3, L4, L5, L6])

q0 = np.array([math.pi/2, 0, 0, math.pi/2, 0, 0])
r = Arm(links, q0, '1-link')
print r.fkine([math.pi/2, 0, 0, math.pi/2, 0, 0])
