import numpy as np
from maddux.objects import Obstacle, Ball
from maddux.environment import Environment
from maddux.robots import simple_human_arm


def obstacle_collision_test():
    obstacle = Obstacle([2.0, 2.0, 0.0], [3.0, 3.0, 1.0])
    ball = Ball([3.0, 3.0, 2.0], 0.25)

    q0 = np.array([0.25, 0.5, 0.5, 0.75, 0, 0, 0])
    human_arm = simple_human_arm(2.0, 2.0, q0, np.array([1.25, 1.25, 0.0]))
    
    env = Environment(dimensions=[10.0, 20.0, 100.0],
                      dynamic_objects=[ball],
                      static_objects=[obstacle],
                      robot=human_arm)
    env.plot()
    
    print "Ball hit obstacle?",
    print obstacle.is_hit_by_sphere(ball.position, ball.radius)

    print "Arm hit obstacle?",
    print human_arm.is_in_collision(obstacle)

    
