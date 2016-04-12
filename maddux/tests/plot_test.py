import numpy as np
from environment import Environment
from objects import Ball, Target
from robots import simple_human_arm

def plot_test():
    q0 = np.array([0.5, 0.2, 0, 0.5, 1.5])
    human_arm = simple_human_arm(2.0, 2.0, q0, np.array([2.0, 2.0, 0.0]))
    
    ball = Ball(np.array([2.0, 0.0, 2.0]), 0.15)
    target = Target(np.array([5.0, 18.0, 2.0]), 0.5)
    env = Environment(ball, target, robot=human_arm,
                      dimensions=[10.0, 20.0, 100.0])

    print human_arm.ikine(ball.position, 10000, 0.01)
    env.plot()
