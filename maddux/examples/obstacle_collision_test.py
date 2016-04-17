import numpy as np
from maddux.objects import Obstacle, Ball
from maddux.environment import Environment
from maddux.robots import simple_human_arm


def obstacle_collision_test():
    obstacles = [Obstacle([1, 2, 1], [2, 2.5, 1.5]),
                 Obstacle([3, 2, 1], [4, 2.5, 1.5])]
    ball = Ball([2.5, 2.5, 2.0], 0.25)

    q0 = np.array([0.25, 0.5, 0.5, 2.0, 0, 0, 0])
    human_arm = simple_human_arm(2.0, 2.0, q0, np.array([1.5, 1.5, 0.0]))
    
    env = Environment(dimensions=[10.0, 20.0, 100.0],
                      dynamic_objects=[ball],
                      static_objects=obstacles,
                      robot=human_arm)

    human_arm.ikine(ball.position)
    env.animate(25.0)
    
    print "Ball hit obstacle?",
    print any([obstacle.is_hit_by_sphere(ball.position, ball.radius) \
               for obstacle in obstacles])

    print "Arm hit obstacle?",
    print any([human_arm.is_in_collision(obstacle) for obstacle in obstacles])

    
