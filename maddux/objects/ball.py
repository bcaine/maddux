"""
A ball object to throw.
"""
import numpy as np
from throwable import ThrowableObject


class Ball(ThrowableObject):

    def __init__(self, position, radius):
        self.radius = radius
        ThrowableObject.__init__(self, position)
    

    def leading_point(self):
        """Return the outermost point on the y axis
           that will hit the target.
        """
        return self.position + np.array([0, self.radius, 0])


    def plot(self, ax):
        """Plots the ball at its current location.

        :param ax: Figure to plot on.
        """
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        x = (2 * self.radius * np.outer(np.cos(u), np.sin(v)) +
              self.position[0])
        y = (2 * self.radius * np.outer(np.sin(u), np.sin(v)) +
              self.position[1])
        z = (2 * self.radius * np.outer(np.ones(np.size(u)), np.cos(v)) +
              self.position[2])
        ax.plot_surface(x, y, z, rstride=4, cstride=4, color='g')
        
