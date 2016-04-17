import numpy as np
from maddux.environment import Environment
from maddux.objects import Ball, Obstacle
from maddux.robots import simple_human_arm


def animate_path(saved_path_file):
    """Load a saved path and animate it"""
    
    obstacles = [Obstacle([1, 2, 1], [2, 2.5, 1.5]),
                 Obstacle([3, 2, 1], [4, 2.5, 1.5])]
    ball = Ball([2.5, 2.5, 2.0], 0.25)
    
    q = np.array([0, 0, 0, np.pi / 2, 0, 0, 0])
    robot = simple_human_arm(2.0, 2.0, q, np.array([3.0, 1.0, 0.0]))
    
    room_dimensions = np.array([10.0, 10.0, 20.0])
    env = Environment(room_dimensions,
                      dynamic_objects=[ball],
                      static_objects=obstacles,
                      robot=robot)

    # Load our saved path
    saved_path = np.load(saved_path_file)

    robot.qs = saved_path
    env.animate(save_path="/home/ben/Development/maddux/test.mp4")
    
    
    
