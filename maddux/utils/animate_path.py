import numpy as np
from maddux.environment import Environment
from maddux.objects import Ball, Obstacle
from maddux.robots import simple_human_arm


def animate_path(input_file, output_file=None):
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
    saved_path = np.load(input_file)

    robot.qs = saved_path

    if output_file is not None:
        env.animate(save_path=output_file)
    else:
        env.animate()
    
    
    
