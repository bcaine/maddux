"""
Random collection of utilities for the robots to use
"""

import numpy as np


def get_rotation_from_homogeneous_transform(transform):
    """Extract the rotation section of the homogeneous transformation

    :param transform: The 4x4 homogeneous transform to extract the
                      rotation matrix from.
    :type transform: numpy.ndarray

    :returns: 3x3 Rotation Matrix
    :rtype: numpy.matrix
    """
    s = transform.shape
    if s[0] != s[1]:
        raise ValueError('Matrix must be a 4x4 homogenous transformation', s)
    n = s[0]
    rotation = transform[0:n - 1, 0:n - 1]
    return rotation


def create_homogeneous_transform_from_point(p):
    """Create a homogeneous transform to move to a given point

    :param p: The (x, y, z) point we want our homogeneous tranform to move to
    :type p: numpy.ndarray

    :returns: 4x4 Homogeneous Transform of a point
    :rtype: numpy.matrix
    """
    I = np.identity(3)
    T = np.vstack((I, np.zeros((3,))))
    p = np.hstack((p, np.ones(1))).reshape((4, 1))
    T = np.hstack((T, p))
    return T


def create_point_from_homogeneous_transform(T):
    """Create a point from a homogeneous transform

    :param T: The 4x4 homogeneous transform
    :type T: numpy matrix

    :returns: The (x, y, z) coordinates of a point from a transform
    :rtype: np.ndarray
    """
    return T[0:3, 3]
