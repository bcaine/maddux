import numpy as np

def plot_sphere_data(position, radius):
    """Given a position and radius, get the data needed to plot.
    :param position: position of sphere
    :param radius: radius of sphere
    """
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    
    x = (2 * radius * np.outer(np.cos(u), np.sin(v)) +
         position[0])
    y = (2 * radius * np.outer(np.sin(u), np.sin(v)) +
         position[1])
    z = (2 * radius * np.outer(np.ones(np.size(u)), np.cos(v)) +
         position[2])

    return (x, y, z)

def plot_sphere(position, radius, ax, color='g'):
    """Plot a sphere.
    :param position: position of sphere
    :param radius: radius of sphere
    :param ax: axes to plot on
    :param color: (Optional) color of sphere
    """
    x, y, z = plot_sphere_data(position, radius)
    return ax.plot_surface(x, y, z, rstride=4, cstride=4, color=color)

    
