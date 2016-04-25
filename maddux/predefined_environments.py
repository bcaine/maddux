import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from maddux.robots import simple_human_arm, noodle_arm
from maddux.environment import Environment
from maddux.objects import Ball, Obstacle, Target
import numpy as np


def get_easy_environment():
    """An easy difficulty environment for planning tests with two obstacles,
    a ball as a target, and a simple human arm.
    """
    obstacles = [Obstacle([1, 2, 1], [2, 2.5, 1.5]),
                 Obstacle([3, 2, 1], [4, 2.5, 1.5])]
    ball = Ball([2.5, 2.5, 2.0], 0.25, target=True)
    q = np.array([0, 0, 0, np.pi / 2, 0, 0, 0])
    robot = simple_human_arm(2.0, 2.0, q, np.array([3.0, 1.0, 0.0]))

    return Environment(dynamic_objects=[ball],
                       static_objects=obstacles,
                       robot=robot)


def get_medium_environment():
    """A medium difficulty environment for planning tests with two obstacles,
    a ball as a target, and a simple human arm.
    """
    obstacles = [Obstacle([2.5, 0, 2.2], [3.5, 1, 2.5]),
                 Obstacle([3, 2, 1], [4, 2.5, 1.5])]
    ball = Ball([2.5, 2.5, 2.0], 0.25, target=True)
    q = np.array([0, 0, 0, 0, 0, 0, 0])
    robot = simple_human_arm(2.0, 2.0, q, np.array([3.0, 1.0, 0.0]))

    return Environment(dynamic_objects=[ball],
                       static_objects=obstacles,
                       robot=robot)


def get_hard_environment():
    """A hard difficulty environment for planning tests with five obstacles,
    a ball as a target, and a simple human arm.
    """
    obstacles = [Obstacle([0.0, 2.0, 0.0], [1.5, 2.5, 3.0]),
                 Obstacle([0.0, 4.0, 0.0], [1.5, 4.5, 3.0]),
                 Obstacle([0.0, 2.5, 0.0], [0.5, 4.0, 3.0]),
                 Obstacle([0.0, 2.0, 3.0], [1.5, 4.5, 3.5]),
                 Obstacle([0.5, 2.5, 0.0], [1.5, 4.0, 1.0])]
    ball = Ball([1.0, 3.25, 2.0], 0.5, target=True)
    q = np.array([0, 0, 0, -np.pi / 2.0, 0, 0, 0])
    robot = simple_human_arm(3.0, 2.0, q, np.array([1.0, 1.0, 0.0]))

    return Environment(dynamic_objects=[ball],
                       static_objects=obstacles,
                       robot=robot)


def get_hard_environment_v2():
    """A very hard difficulty environment for planning tests with three
    obstacles, a ball as a target, and a simple human arm.
    """
    obstacles = [Obstacle([2.5, 2.0, 0.0], [4.0, 2.5, 4.0]),
                 Obstacle([1.5, 2.0, 0.0], [2.5, 3.5, 4.0]),
                 Obstacle([3.2, 3.5, 0.0], [5.5, 4.0, 4.0])]
    ball = Ball([2.8, 3.8, 2.0], 0.25, target=True)
    q = np.array([0, 0, 0, 0, 0, 0, 0])
    robot = simple_human_arm(2.0, 2.0, q, np.array([3.0, 3.0, 0.0]))

    return Environment(dynamic_objects=[ball],
                       static_objects=obstacles,
                       robot=robot)


def get_noodle_environment():
    """An absurd environment for our noodle arm to do planning tests. It has
    five obstacles, a ball as a target, and our 10 link noodle arm
    """
    obstacles = [Obstacle([0.0, 2.0, 0.0], [1.5, 2.5, 3.0]),
                 Obstacle([4.0, 4.0, 0.0], [4.5, 4.5, 3.0]),
                 Obstacle([5.0, 0, 2.0], [5.5, 0.5, 3.0]),
                 Obstacle([2.0, 2.0, 3.0], [5.0, 2.5, 3.5]),
                 Obstacle([3.0, 4.5, 6.0], [7.0, 6.0, 5.0])]
    ball = Ball([5.0, 5.0, 3.0], 0.5, target=True)
    q = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    seg_lengths = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    robot = noodle_arm(seg_lengths, q, np.array([3.0, 1.0, 0.0]))

    return Environment(dynamic_objects=[ball],
                       static_objects=obstacles,
                       robot=robot)


def get_tutorial_environment():
    """Our environment from our documentation tutorial"""
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
    return Environment(dimensions=[10, 10, 10],
                       dynamic_objects=[ball],
                       static_objects=[target, obstacle],
                       robot=arm)


environments = {
    "easy": get_easy_environment,
    "medium": get_medium_environment,
    "hard": get_hard_environment,
    "hard_v2": get_hard_environment_v2,
    "noodle": get_noodle_environment,
    "tutorial": get_tutorial_environment,
}
