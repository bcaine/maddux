from vpython import *


def sphere(position, radius):
    """Plot a sphere
    :param position: Position of sphere
    :param radius: Radius of sphere
    """
    x, y, z = position
    return sphere(pos = vector(x, y, z), radius=radius, color=color.cyan)    


def box(p1, p2):
    x, y, z = p1
    L = x + p2[0]
    H = y + p2[1]
    W = z + p2[2]
    return box(pos=vector(x, y, z), axis=vector(0, 0, 0),
               length=L, height=H, width=W)


    
