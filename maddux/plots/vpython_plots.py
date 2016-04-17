import vpython


def sphere(position, radius):
    """Plot a sphere
    :param position: Position of sphere
    :param radius: Radius of sphere
    """
    x, y, z = position
    return vpython.sphere(pos=vpython.vector(x, y, z),
                          radius=radius, color=vpython.color.cyan)    


def box(p1, p2):
    x, y, z = p1
    L = x + p2[0]
    H = y + p2[1]
    W = z + p2[2]
    return vpython.box(pos=vpython.vector(x, y, z),
                       axis=vpython.vector(0, 0, 0),
                       length=L, height=H, width=W)

def cylinder(p1, p2, radius=5):
    """Plot a 3d line with a specified thickness
    :param p1: One endpoint
    :param p2: The other endpoint
    :param radius: Default 5. Radius of Cylinder
    """
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    ax, ay, az = x2 - x1, y2 - y1, z2 - z1
    
    return vpython.cylinder(pos=vpython.vector(x1, y1, z1),
                            axis=vpython.vector(ax, ay, az),
                            radius=radius,
                            color=vpython.color.cyan)
