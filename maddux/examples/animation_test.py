import numpy as np
from environment import Environment
from objects import Ball, Target
from robots import simple_human_arm


def ball_animation_test():
    balls = []
    for _ in xrange(10):
        ball = Ball(np.random.rand(3) * 10, 0.15)
        ball.throw(np.random.uniform(-10, 10, 3))
        balls.append(ball)
    target = Target(np.array([5.0, 18.0, 2.0]), 0.5)
    env = Environment(dimensions=[10.0, 20.0, 100.0],
                      dynamic_objects=balls, static_objects=[target])
    env.animate(3.0)

def arm_animation_test():
    q0 = np.array([0.5, 0.2, 0, 0.5, 1.5])
    human_arm = simple_human_arm(2.0, 2.0, q0, np.array([2.0, 2.0, 0.0]))

    ball = Ball(np.array([3.0, 2.0, 3.0]), 0.15)
    env = Environment([5.0, 5.0, 5.0], dynamic_objects=[ball],
                      robot=human_arm)

    human_arm.ikine(ball.position)
    env.animate(3.0)

def arm_ball_animation_test():
    q0 = np.array([0.5, 0.2, 0, 0.5, 1.5])
    human_arm = simple_human_arm(2.0, 2.0, q0, np.array([2.0, 2.0, 0.0]))
    ball = Ball(np.array([0.0, 0.0, 0.0]), 0.15)

    human_arm.hold(ball)
    
    env = Environment([5.0, 5.0, 5.0], dynamic_objects=[ball],
                      robot=human_arm)

    position = human_arm.ikine([3.0, 2.0, 3.0])
    env.animate(3.0)
    
