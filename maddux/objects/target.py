"""
A stationary object that something may collide with.
"""
from maddux.objects.static import StaticObject
import numpy as np

HIT_ERROR = 0.01


class Target(StaticObject):

    def __init__(self, position, radius):
        """
        Target Init

        :param position: Position of center
        :type position: 1x3 numpy.ndarray

        :param radius: radius of target
        :type radius: int

        :rtype: None
        """
        self.position = np.array(position)
        self.radius = radius
        self.target = True

    def is_hit(self, position):
        """Check if the target is hit.

        :param position: A object's position
        :type position: numpy.array

        :rtype: Boolean
        """
        diff = np.absolute(position - self.position)

        x_hit = diff[0] <= self.radius
        y_hit = diff[1] <= HIT_ERROR
        z_hit = diff[2] <= self.radius
        return x_hit and y_hit and z_hit

    def display(self):
        """
        Display target properties
        :rtpye: None
        """
        print("Position: {}".format(self.position))
        print("Radius: {}".format(self.radius))

    def plot_data(self):
        """
        Gets the plot data at the targets location
        :rtype: 3-tuple of integers
        """
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        x = (2 * self.radius * np.outer(np.cos(u), np.sin(v)) +
             self.position[0])
        y = self.position[1]
        z = (2 * self.radius * np.outer(np.ones(np.size(u)), np.cos(v)) +
             self.position[2])
        return (x, y, z)

    def plot(self, ax):
        """
        Plots the target at its location.
        :param ax: Figure to plot on.
        :type ax: matplotlib figure
        :rtype: matplotlib figure
        """
        x, y, z = self.plot_data()
        return ax.plot_surface(x, y, z, color='b', linewidth=0, alpha=0.25)
