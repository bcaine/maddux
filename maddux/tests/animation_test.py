import numpy as np

from maddux import Environment
from maddux.objects import Ball, Target

ball = Ball(np.array([2.0, 0.0, 2.0]), 0.15)
ball.throw([0, 3.5, 15.0])

target = Target(np.array([2.0, 10.0, 2.0]), 0.5)
env = Environment(ball, target)

env.animate(100)
