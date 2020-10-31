"""
A stationary rectangular solid that something may collide with
"""
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from maddux.objects.static import StaticObject


class Obstacle(StaticObject):

    def __init__(self, pt1, pt2, color='r'):
        """Create a 3D Rectangle from 2 points

        :param pt1: The first point (x, y, z) defining the rect
        :type pt1: numpy.ndarray

        :param pt2: The second point (x, y, z) defining the rect
        :type pt2: numpy.ndarray

        :param color: color of the obstacle
        :type color: str

        :rtype: None
        """
        self.pt1 = pt1
        self.pt2 = pt2
        self.color = color

    # TODO: Make this use numpy arrays instead of lists
    def get_paths(self):
        """Returns the paths for each of the surfaces of the
        rectangle for plotting.

        :returns (bottom, top, front, back, left, right)
        :rtype: list of 6 4x3 numpy.ndarrays
        """
        [x1, y1, z1] = self.pt1
        [x2, y2, z2] = self.pt2
        pt1 = [x1, y1, z1]
        pt2 = [x1, y1, z2]
        pt3 = [x1, y2, z1]
        pt4 = [x1, y2, z2]
        pt5 = [x2, y1, z1]
        pt6 = [x2, y1, z2]
        pt7 = [x2, y2, z1]
        pt8 = [x2, y2, z2]

        bottom = [pt1, pt3, pt7, pt5]
        top = [pt2, pt4, pt8, pt6]
        front = [pt1, pt2, pt6, pt5]
        back = [pt3, pt4, pt8, pt7]
        left = [pt1, pt2, pt4, pt3]
        right = [pt5, pt6, pt8, pt7]
        paths = [bottom, top, front, back, left, right]
        return paths

    def is_hit(self, position):
        """Checks if the rectangle is hit by a point or path

        :param position: An objects position (x, y, z) or positions if
                         it is a path([x1, x2, ..], [y1, y2, ..], [z1, z2, ..]
        :type position: numpy.ndarray or numpy.matrix

        :returns: Whether the obstacle was hit by a point or path
        :rtype: bool
        """
        is_point = len(position.shape) == 1

        if is_point:
            x, y, z = position
        else:
            assert position.shape[1] == 3
            x = position[:, 0]
            y = position[:, 1]
            z = position[:, 2]

        [x1, y1, z1] = self.pt1
        [x2, y2, z2] = self.pt2

        x_hit = (x >= x1) & (x <= x2)
        y_hit = (y >= y1) & (y <= y2)
        z_hit = (z >= z1) & (z <= z2)

        all_hit = x_hit & y_hit & z_hit

        if is_point:
            return (x_hit and y_hit and z_hit)
        else:
            return np.any(all_hit)

    def is_hit_by_sphere(self, center, radius):
        """Checks if the rectangle is hit by a sphere

        :param center: Sphere's center (x, y, z)
        :type center: numpy.ndarray

        :param radius: The sphere's radius
        :type radius: int

        :returns: Whether obstacle was hit by a sphere
        :rtype: bool
        """

        [x1, y1, z1] = self.pt1
        [x2, y2, z2] = self.pt2
        x, y, z = center

        x_hit = (x + radius >= x1) & (x - radius <= x2)
        y_hit = (y + radius >= y1) & (y - radius <= y2)
        z_hit = (z + radius >= z1) & (z - radius <= z2)

        return x_hit and y_hit and z_hit

    def display(self):
        """Display obstacle properties

        :rtype: None
        """
        print("Center: {}".format(self.center))
        print("Width: {}".format(self.width))
        print("Height: {}".format(self.height))
        print("Depth: {}".format(self.depth))

    def plot(self, ax):
        """Plots the obstacle at its location

        :param ax: Figure to plot on
        :type ax: matplotlib.axes

        :rtpye: None
        """
        paths = self.get_paths()
        rectangle = Poly3DCollection(paths, facecolors=self.color)
        ax.add_collection3d(rectangle)
