import numpy as np
from maddux.robots.predefined_robots import simple_human_arm
from maddux.objects import Ball, Target, Obstacle
from maddux.environment import Environment


def tutorial():
    """Code from our tutorial on the documentation"""
    
    # Create an arm with a specific config and base position
    q0 = np.array([0.5, 0.2, 0, 0.5, 0, 0, 0])
    base_pos = np.array([2.0, 2.0, 0.0])
    
    # And link segments of length 2.0
    arm = simple_human_arm(2.0, 2.0, q0, base_pos)
    
    # We then create a ball, target, and obstacle
    ball = Ball(position=[2.0, 0.0, 2.0], radius=0.15)
    target = Target(position=[5.0, 8.0, 2.0], radius=0.5)
    obstacle = Obstacle([4, 4, 0], [5, 5, 2])

    # And use these to create an environment with dimensions 10x10x10
    env = Environment(dimensions=[10, 10, 10],
                      dynamic_objects=[ball],
                      static_objects=[target, obstacle],
                      robot=arm)
    
    arm.ikine(ball.position)
    env.animate(3.0)
    arm.save_path("tutorial_path")

if __name__ == '__main__':
    tutorial()
