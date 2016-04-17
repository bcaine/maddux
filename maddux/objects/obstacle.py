"""
A stationary rectangular solid that something may collide with
"""
from static import StaticObject
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Obstacle(StaticObject):

    def __init__(self, pt1, pt2):
        """
        """
        self.pt1 = pt1
        self.pt2 = pt2

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
        :param position: A object's position
        """
        [x1, y1, z1] = self.pt1
        [x2, y2, z2] = self.pt2
        x, y, z = position
        x_hit = x1 <= x <= x2
        y_hit = y1 <= y <= y2
        z_hit = z1 <= z <= z2
        return not (x_hit and y_hit and z_hit)

    def is_hit_by_sphere(self, center, radius):
        """
        Checks if the rectangle is hit by a sphere
        :param center: 1x3 numpy array of sphere's center
        :param radius: the sphere's radius
        """
        dmin = 0
        for i in range(3):
            if center[i]< self.pt1[i]:
              dmin += (center[i] - self.pt1[i]) ** 2
            elif center[i] > self.pt[2]:
              dmin += (center[i] - self.pt2[i]) ** 2
        return dmin <= radius ** 2

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
        rectangle = Poly3DCollection(paths)
        ax.add_collection3d(rectangle)
