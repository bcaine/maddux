import numpy as np


def plot_sphere_data(position, radius):
    """Given a position and radius, get the data needed to plot.
    :param position: position of sphere
    :type position: 1x3 numpy.array
    :param radius: radius of sphere
    :type radius: integer
    :rtype: 3-tuple of numpy.array
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


def plot_sphere(position, radius, ax, color='g', linewidth=0):
    """Plot a sphere.
    :param position: position of sphere
    :type position: 1x3 numpy.array
    :param radius: radius of sphere
    :type radius: integer
    :param ax: axes to plot on
    :type ax: matplotlib figure
    :param color: (Optional) color of sphere
    :type color: String
    :param linewidth: (Optional) width of ball gridlines
    :type linewidth: integer
    :rtype: matplotlib figure
    """
    x, y, z = plot_sphere_data(position, radius)
    return ax.plot_surface(x, y, z, rstride=4, cstride=4,
                           color=color, linewidth=0)
