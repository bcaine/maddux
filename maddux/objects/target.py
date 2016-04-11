"""
A stationary object that something may collide with.
"""
import numpy as np

HIT_ERROR = 0.01

class Target:

    def __init__(self, position, radius):
        """Target Init
        :param position: 1x3 numpy array of position of center
        :param radius: radius of target
        """
        self.position = np.array(position)
        self.radius = radius


    def get_score(self, position):
        """Given an object position hitting the target, return the score"""
        distance = np.linalg.norm(position - self.position)
        score = 0.75 ** distance
        if self.is_hit(position):
            return 10 * score
        else:
            return score


    def is_hit(self, position):
        """Check if the target is hit.
        :param position: A ball object's position
        """
        diff = np.absolute(position - self.position)

        x_hit = diff[0] <= self.radius
        y_hit = diff[1] <= HIT_ERROR
        z_hit = diff[2] <= self.radius
        return x_hit and y_hit and z_hit


    def display(self):
        print "Position: {}".format(self.position)
        print "Radius: {}".format(self.radius)


    def plot_data(self):
        """Gets the plot data at the targets location"""
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        x = (2 * self.radius * np.outer(np.cos(u), np.sin(v)) +
             self.position[0])
        y = self.position[1]
        z = (2 * self.radius * np.outer(np.ones(np.size(u)), np.cos(v)) +
             self.position[2])
        return (x, y, z)


    def plot(self, ax):
        """Plots the target at its location.

        :param ax: Figure to plot on.
        """
        x, y, z = self.plot_data()
        return ax.plot_surface(x, y, z, color='b', linewidth=0, alpha=0.25)
