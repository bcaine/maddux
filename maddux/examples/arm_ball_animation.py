import numpy as np
from maddux.environment import Environment
from maddux.objects import Ball, Target
from maddux.robots import simple_human_arm

def arm_ball_animation():
    """Animate an arm holding a ball, moving around to an arbitrary spot."""

    # Create a human arm
    q0 = np.array([0.5, 0.2, 0, 0.5, 1.5])
    human_arm = simple_human_arm(2.0, 2.0, q0, np.array([2.0, 2.0, 0.0]))
    
    # Create a ball the arm can hold
    ball = Ball(np.array([0.0, 0.0, 0.0]), 0.15)
    human_arm.hold(ball)
    
    # Declare our environment
    env = Environment([5.0, 5.0, 5.0], dynamic_objects=[ball],
                      robot=human_arm)
    
    # Find joint config to random location show we can show arm moving
    # while holding the ball
    position = human_arm.ikine([3.0, 2.0, 3.0])

    # Animate for 3 seconds
    env.animate(3.0)

if __name__ == '__main__':
    arm_ball_animation()
