import numpy as np
from maddux.objects import Obstacle, Ball
from maddux.environment import Environment
from maddux.robots import simple_human_arm

def obstacle_collision():
    """Tests whether an arm in its final configuration makes contact 
    with either of our obstacles.
    """

    # Create two obstacles
    obstacles = [Obstacle([1, 4, 1], [4, 5, 1.5]),
                 Obstacle([1, 2, 1], [4, 3, 1.5])]
    # And a ball
    ball = Ball([2.5, 2.5, 2.0], 0.25)
    
    # Create an arm
    q0 = np.array([0, 0, 0, np.pi / 2, 0, 0, 0])
    human_arm = simple_human_arm(2.0, 2.0, q0, np.array([3.0, 1.0, 0.0]))
    
    # Define environment
    env = Environment(dimensions=[10.0, 10.0, 20.0],
                      dynamic_objects=[ball],
                      static_objects=obstacles,
                      robot=human_arm)
    
    # Run inverse kinematics towards the ball
    human_arm.ikine(ball.position)
    
    # And animate it for 5 seconds
    env.animate(5.0)
    
    print "Ball hit obstacle?",
    print any([obstacle.is_hit_by_sphere(ball.position, ball.radius)
               for obstacle in obstacles])
    
    print "Arm link hit obstacle?",
    print any([human_arm.is_in_collision(obstacle) for obstacle in obstacles])

if __name__ == '__main__':
    obstacle_collision()
