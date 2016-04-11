import numpy as np
from environment import Environment
from objects import Ball, Target

ball = Ball(np.array([2.0, 0.0, 2.0]), 0.15)
target = Target(np.array([5.0, 18.0, 2.0]), 0.5)
env = Environment(ball, target, dimensions=[10.0, 20.0, 100.0])

ball.throw([1.75, 11.5, 7.8])
env.animate(3.0)

ball.display()
target.display()

leading = np.array([0, 0.15, 0])
diff = np.absolute(ball.positions + leading - target.position)
is_hit = [target.is_hit(pos + leading) for pos in ball.positions]

min_location = [i for i, val in enumerate(diff.sum(axis=1) < (diff.sum(axis=1).min() + 0.01)) if val][0]

if any(is_hit):
    print "Collision Location: {}".format(ball.positions[min_location])
else:
    print "No collision. Closest: {}".format(ball.positions[min_location])
