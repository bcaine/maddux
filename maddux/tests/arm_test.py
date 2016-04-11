from robots.link import Link
from robots.arm import Arm
import numpy as np


np.set_printoptions(suppress=True)

L1 = Link(0, 0, 0, 1.571)
L2 = Link(0, 0, 0, -1.571)
L3 = Link(0, 0.4318, 0, -1.571)
L4 = Link(0, 0, 0, 1.571)
L5 = Link(0, 0.4318, 0, 1.571)
links = np.array([L1, L2, L3, L4, L5])

q0 = np.array([0, 0, 0, np.pi / 2, 0])
r = Arm(links, q0, '1-link')
print r.jacob0([0, 0, 0, np.pi / 2, 0])
