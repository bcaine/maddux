import unittest
import math
import numpy as np
from robots import simple_human_arm

class ArmTest(unittest.TestCase):
    def test_fkine(self):
        q0 = [0, math.pi/4, 0, -math.pi/4, math.pi/2]
        r = simple_human_arm(2, 1, q0)

        fkine_sol1 = np.array([[0.0, -1.0, 0.0, -2.4142],
                               [1.0,  0.0, 0.0, 0.0    ],
                               [0.0,  0.0, 1.0, 1.4142 ],
                               [0.0,  0.0, 0.0, 1.0    ]])
        self.assertLess(np.linalg.norm(r.fkine() - fkine_sol1), 1.0)

    #def test_ikine:

    #def test_jacobn:

    #def test_jacob0
