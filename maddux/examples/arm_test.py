import numpy as np
import math
from maddux.robots import simple_human_arm


def arm_test():
    np.set_printoptions(suppress=True)

    q0 = np.array([0, math.pi / 4, 0, -math.pi / 4, math.pi / 2])
    r = simple_human_arm(2, 1, q0)
    #print r.ikine(np.array([1, 1, 1]), 10000, 0.01)
    print r.jacob0(q0)
