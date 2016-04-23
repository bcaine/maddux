import numpy as np
from maddux.environment import Environment
from maddux.objects import Ball, Target

def ball_animation():
    """Create a few balls and have them all move around the environment
    at different velocities.
    """

    # Create 5 balls moving at random velocities
    balls = []
    for _ in xrange(5):
        # Create a ball at a random starting position
        starting_pos = np.random.rand(3) * 10
        ball = Ball(starting_pos, radius=0.15)
        
        # And generate a random velocity to "throw" it at
        velocity = np.random.uniform(-10, 10, 3)
        ball.throw(velocity)

        # Add it on the list we will feed to the environment
        balls.append(ball)

    # Add a target, just to show one
    target = Target(np.array([5.0, 18.0, 2.0]), 0.5)
    
    # Declare an environment with our room, balls, and target
    env = Environment(dimensions=[10.0, 20.0, 100.0],
                      dynamic_objects=balls, static_objects=[target])
    
    # Animate it for 5 seconds.
    env.animate(5.0)

if __name__ == '__main__':
    ball_animation()
