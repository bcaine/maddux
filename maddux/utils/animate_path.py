import numpy as np
from maddux.environment import Environment
from maddux.objects import Ball, Obstacle
from maddux.robots import simple_human_arm
from maddux.rl_experiments.environments import environments


def animate_path(environment, input_file, output_file=None):
    """Load a saved path and animate it"""
    if environment in environments:
        env = environments[environment]()
    else:
        print "Please provide an environment from: {}".format(
            environments.keys())
        return

    # Load our saved path
    saved_path = np.load(input_file)
    env.robot.qs = saved_path

    if output_file is not None:
        env.animate(save_path=output_file)
    else:
        env.animate()
    
    
    
