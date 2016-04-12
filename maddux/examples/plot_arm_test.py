import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3

from maddux.robots import simple_human_arm

def plot_arm_test():
    q0 = np.array([1.5, 0.2, 0, 0.5, 1.5])
    human_arm = simple_human_arm(2.0, 1.0, q0)

    fig = plt.figure()
    ax = p3.Axes3D(fig)
    ax.set_xlim([0, 3])
    ax.set_ylim([0, 3])
    ax.set_zlim([0, 3])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    for link in human_arm.links:
        link.plot(ax)

    plt.show()
