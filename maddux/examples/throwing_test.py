import numpy as np
from maddux.environment import Environment
from maddux.objects import Ball, Target
from maddux.robots import simple_human_arm

def throwing_test():
    q0 = np.array([0, 0, 0, 0, 0])
    human_arm = simple_human_arm(2.0, 2.0, q0, np.array([2.0, 2.0, 4.0]))

    ball = Ball(np.array([0, 0, 0]), 0.15)
    target = Target(np.array([2.0, 10.0, 2.0]), 0.5)
    env = Environment([10.0, 10.0, 50.0], dynamic_objects=[ball],
                      static_objects=[target], robot=human_arm)

    human_arm.hold(ball)
    # human_arm.ikine(np.array([3.0, 1.0, 1.0]))

    
    env.animate(25.0)

