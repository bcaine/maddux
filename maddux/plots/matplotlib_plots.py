import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def sphere_data(position, radius):
    """Given a position and radius, get the data needed to plot.
    :param position: position of sphere
    :param radius: radius of sphere
    """
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    x = (radius * np.outer(np.cos(u), np.sin(v)) +
         position[0])
    y = (radius * np.outer(np.sin(u), np.sin(v)) +
         position[1])
    z = (radius * np.outer(np.ones(np.size(u)), np.cos(v)) +
         position[2])

    return (x, y, z)


def sphere(position, radius, ax=None, color='g', linewidth=0):
    """Plot a sphere.
    :param position: position of sphere
    :param radius: radius of sphere
    :param ax: axes to plot on
    :param color: (Optional) color of sphere
    :param linewidth: (Optional) width of ball gridlines
    """
    x, y, z = sphere_data(position, radius)
    return ax.plot_surface(x, y, z, rstride=4, cstride=4,
                           color=color, linewidth=0)


def box_data(p1, p2):
    """Given two points, get planes we want to plot
    :param p1: Point 1 of the rectangle (one corner)
    :param p2: Point 2 of the recangle (opposite corner)
    """
    [x1, y1, z1] = p1
    [x2, y2, z2] = p2
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


def box(p1, p2, ax):
    """Plot a 3d rectangle
    :param p1: Point 1 of the rectangle (one corner)
    :param p2: Point 2 of rectangle (opposite corner)
    :param ax: Axis to plot on
    """
    
    data = box_data(p1, p2)
    rectangle = Poly3DCollection(data)
    return ax.add_collection3d(rectangle)
