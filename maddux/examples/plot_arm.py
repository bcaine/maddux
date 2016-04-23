import numpy as np
from maddux.environment import Environment
from maddux.robots import simple_human_arm

def plot_arm():
    """Shows how to plot an arm."""

    # Create an arm at a certain position and joint angle
    q0 = np.array([0, 0, 0, -2.0, 0, 0, 0])
    base_pos = np.array([1.0, 1.0, 0.0])
    human_arm = simple_human_arm(2.0, 1.0, q0, base_pos)
    
    env = Environment(dimensions=[3.0, 3.0, 3.0], robot=human_arm)
    env.plot()

if __name__ == '__main__':
    plot_arm()
