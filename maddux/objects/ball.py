"""
A ball object to throw.
"""
import numpy as np
from maddux.objects.throwable import ThrowableObject
from maddux.plot import plot_sphere


class Ball(ThrowableObject):

    def __init__(self, position, radius, target=False):
        """Ball object that can move, have a velocity, and hit objects

        :param position: The position (x,y,z) of the center of the ball
        :type position: numpy.ndarray

        :param: radius: The radius of the ball
        :type radius: int

        :rtype: None
        """
        self.radius = radius
        ThrowableObject.__init__(self, position, target)

    def plot(self, ax):
        """Plots the ball at its current location.

        :param ax: Figure to plot on.
        :type ax: matplotlib.axes

        :returns: Matplotlib figure
        :rtype: matplotlib.axes
        """
        return plot_sphere(self.position, self.radius, ax)
