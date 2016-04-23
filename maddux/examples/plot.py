import numpy as np
from maddux.environment import Environment
from maddux.objects import Ball, Target
from maddux.robots import simple_human_arm

def plot():
    """Generic plotting example given an environment with some
    objects in it and a robot.
    """

    # Create our arm
    q0 = np.array([0.5, 0.2, 0, 0.5, 0, 0, 0])
    human_arm = simple_human_arm(2.0, 2.0, q0, np.array([2.0, 2.0, 0.0]))
    
    # And our objects
    ball = Ball(np.array([2.0, 0.0, 2.0]), 0.15)
    target = Target(np.array([5.0, 8.0, 2.0]), 0.5)
    env = Environment(dimensions=[10.0, 10.0, 10.0],
                      dynamic_objects=[ball],
                      static_objects=[target],
                      robot=human_arm)
    
    # Make the arm touch the ball
    new_q = human_arm.ikine(ball.position, 10000, 0.01)
    human_arm.update_angles(new_q)
    
    # Plot it
    env.plot()

if __name__ == '__main__':
    plot()
