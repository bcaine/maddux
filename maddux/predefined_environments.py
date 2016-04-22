import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from maddux.robots import simple_human_arm, noodle_arm
from maddux.environment import Environment
from maddux.objects import Ball, Obstacle
import numpy as np

room_dimensions = np.array([10.0, 10.0, 10.0])


def get_easy_environment():
    obstacles = [Obstacle([1, 2, 1], [2, 2.5, 1.5]),
                 Obstacle([3, 2, 1], [4, 2.5, 1.5])]
    ball = Ball([2.5, 2.5, 2.0], 0.25)
    q = np.array([0, 0, 0, np.pi / 2, 0, 0, 0])
    robot = simple_human_arm(2.0, 2.0, q, np.array([3.0, 1.0, 0.0]))

    return Environment(room_dimensions,
                       dynamic_objects=[ball],
                       static_objects=obstacles,
                       robot=robot)


def get_medium_environment():
    obstacles = [Obstacle([2.5, 0, 2.2], [3.5, 1, 2.5]),
                 Obstacle([3, 2, 1], [4, 2.5, 1.5])]
    ball = Ball([2.5, 2.5, 2.0], 0.25)
    q = np.array([0, 0, 0, 0, 0, 0, 0])
    robot = simple_human_arm(2.0, 2.0, q, np.array([3.0, 1.0, 0.0]))

    return Environment(room_dimensions,
                       dynamic_objects=[ball],
                       static_objects=obstacles,
                       robot=robot)


def get_hard_environment():
    obstacles = [Obstacle([0.0, 2.0, 0.0], [1.5, 2.5, 3.0]),
                 Obstacle([0.0, 4.0, 0.0], [1.5, 4.5, 3.0]),
                 Obstacle([0.0, 2.5, 0.0], [0.5, 4.0, 3.0]),
                 Obstacle([0.0, 2.0, 3.0], [1.5, 4.5, 3.5]),
                 Obstacle([0.5, 2.5, 0.0], [1.5, 4.0, 1.0])]
    ball = Ball([1.0, 3.25, 2.0], 0.5)
    q = np.array([0, 0, 0, -np.pi / 2.0, 0, 0, 0])
    robot = simple_human_arm(3.0, 2.0, q, np.array([1.0, 1.0, 0.0]))

    return Environment(room_dimensions,
                       dynamic_objects=[ball],
                       static_objects=obstacles,
                       robot=robot)


def get_very_hard_environment():
    obstacles = [Obstacle([2.5, 2.0, 0.0], [4.0, 2.5, 4.0]),
                 Obstacle([1.5, 2.0, 0.0], [2.5, 3.5, 4.0]),
                 Obstacle([3.2, 3.5, 0.0], [5.5, 4.0, 4.0])]
    ball = Ball([2.8, 3.8, 2.0], 0.25)
    q = np.array([0, 0, 0, 0, 0, 0, 0])
    robot = simple_human_arm(2.0, 2.0, q, np.array([3.0, 3.0, 0.0]))

    return Environment(room_dimensions,
                       dynamic_objects=[ball],
                       static_objects=obstacles,
                       robot=robot)


def get_noodle_environment():
    obstacles = [Obstacle([0.0, 2.0, 0.0], [1.5, 2.5, 3.0]),
                 Obstacle([4.0, 4.0, 0.0], [4.5, 4.5, 3.0]),
                 Obstacle([5.0, 0, 2.0], [5.5, 0.5, 3.0]),
                 Obstacle([2.0, 2.0, 3.0], [5.0, 2.5, 3.5]),
                 Obstacle([3.0, 4.5, 6.0], [7.0, 6.0, 5.0])]
    ball = Ball([5.0, 5.0, 3.0], 0.5)
    q = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    seg_lengths = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    robot = noodle_arm(seg_lengths, q, np.array([3.0, 1.0, 0.0]))

    return Environment(room_dimensions,
                       dynamic_objects=[ball],
                       static_objects=obstacles,
                       robot=robot)


predefined_environments = {
    "easy": get_easy_environment,
    "medium": get_medium_environment,
    "hard": get_hard_environment,
    "very_hard": get_very_hard_environment,
    "noodle": get_noodle_environment,
}
