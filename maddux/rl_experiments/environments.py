import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from maddux.robots import simple_human_arm
from maddux.environment import Environment
from maddux.objects import Ball, Obstacle
import numpy as np

room_dimensions = np.array([10.0, 10.0, 10.0])

def get_easy_environment():
    easy_obstacles = [Obstacle([1, 2, 1], [2, 2.5, 1.5]),
                        Obstacle([3, 2, 1], [4, 2.5, 1.5])]
    easy_ball = Ball([2.5, 2.5, 2.0], 0.25)
    easy_q = np.array([0, 0, 0, np.pi / 2, 0, 0, 0])
    easy_robot = easy_human_arm(2.0, 2.0, easy_q,
                                    np.array([3.0, 1.0, 0.0]))

    return Environment(room_dimensions,
                       dynamic_objects=[easy_ball],
                       static_objects=easy_obstacles,
                       robot=easy_robot)

def get_medium_environment():
    medium_obstacles = [Obstacle([2.5, 0, 2.2], [3.5, 1, 2.5]),
                        Obstacle([3, 2, 1], [4, 2.5, 1.5])]
    medium_ball = Ball([2.5, 2.5, 2.0], 0.25)
    medium_q = np.array([0, 0, 0, 0, 0, 0, 0])
    medium_robot = easy_human_arm(2.0, 2.0, medium_q,
                                    np.array([3.0, 1.0, 0.0]))

    return Environment(room_dimensions,
                       dynamic_objects=[medium_ball],
                       static_objects=medium_obstacles,
                       robot=medium_robot)

def get_hard_environment():
    hard_obstacles = [Obstacle([0.0, 2.0, 0.0], [1.5, 2.5, 3.0]),
                      Obstacle([0.0, 4.0, 0.0], [1.5, 4.5, 3.0]),
                      Obstacle([0.0, 2.5, 0.0], [0.5, 4.0, 3.0]),
                      Obstacle([0.0, 2.0, 3.0], [1.5, 4.5, 3.5]),
                      Obstacle([0.5, 2.5, 0.0], [1.5, 4.0, 1.0])]
    hard_ball = Ball([1.0, 3.25, 2.0], 0.5)
    hard_q = np.array([0, 0, 0, -np.pi/2.0, 0, 0, 0])
    hard_robot = easy_human_arm(3.0, 2.0, hard_q, np.array([1.0, 1.0, 0.0]))

    return Environment(room_dimensions,
                       dynamic_objects=[hard_ball],
                       static_objects=hard_obstacles,
                       robot=hard_robot)

environments = {
    "easy": get_easy_environment,
    "medium": get_medium_environment,
    "hard": get_hard_environment,
}


