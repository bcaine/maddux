import numpy as np


def plot_sphere_data(position, radius):
    """Given a position and radius, get the data needed to plot.

    :param position: Position in (x, y, z) of sphere
    :type position: numpy.ndarray

    :param radius: radius of sphere
    :type radius: int

    :returns: (x, y, z) tuple of sphere data to use to create a surface
    :rtype: (np.ndarray, np.ndarray, np.ndarray)
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

    :param position: Position in (x, y, z) of sphere
    :type position: numpy.ndarray

    :param radius: radius of sphere
    :type radius: int

    :param ax: axes to plot on
    :type ax: matplotlib.axes

    :param color: (Optional) color of sphere
    :type color: str

    :param linewidth: (Optional) width of ball gridlines
    :type linewidth: int

    :rtype: matplotlib.axes
    """
    x, y, z = plot_sphere_data(position, radius)
    return ax.plot_surface(x, y, z, rstride=4, cstride=4,
                           color=color, linewidth=0)
