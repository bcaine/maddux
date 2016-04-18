"""
A stationary rectangular solid that something may collide with
"""
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from static import StaticObject


class Obstacle(StaticObject):

    def __init__(self, pt1, pt2, color='r'):
        """
        """
        self.pt1 = pt1
        self.pt2 = pt2
        self.color = color

    def get_paths(self):
      """
      Returns the paths for each of the surfaces of the
      rectangle for plotting
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
        """
        Checks if the rectangle is hit
        :param position: A vector representing an objects position or
                         positions (if its a path)
        """
        # TODO: Clean this up, its pretty gross
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
        """
        Checks if the rectangle is hit by a sphere
        :param center: 1x3 numpy array of sphere's center
        :param radius: the sphere's radius
        """

        [x1, y1, z1] = self.pt1
        [x2, y2, z2] = self.pt2
        x, y, z = center

        x_hit = (x + radius >= x1) & (x - radius <= x2)
        y_hit = (y + radius >= y1) & (y - radius <= y2)
        z_hit = (z + radius >= z1) & (z - radius <= z2)

        return x_hit and y_hit and z_hit

    def display(self):
        print "Center: {}".format(self.center)
        print "Width: {}".format(self.width)
        print "Height: {}".format(self.height)
        print "Depth: {}".format(self.depth)

    def plot(self, ax):
        """
        Plots the obstacle at its location
        :param ax: Figure to plot on
        """
        paths = self.get_paths()
        rectangle = Poly3DCollection(paths, facecolors=self.color)
        ax.add_collection3d(rectangle)
