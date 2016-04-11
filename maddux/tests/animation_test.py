import numpy as np

from environment import Environment
from objects import Ball, Target

ball = Ball(np.array([2.0, 0.0, 2.0]), 0.15)
target = Target(np.array([2.0, 10.0, 2.0]), 0.5)
env = Environment(ball, target)

ball.throw([0, 3.5, 15.0])
env.animate(1000)


