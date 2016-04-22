"""
Random collection of utilities for the robots to use
"""

import numpy as np


def get_rotation_from_homogeneous_transform(transform):
    """
    Extract the rotation section of the homogeneous transformation
    :param transform: The homogeneous transform to extract the rotation
                      matrix from
    :type transform: 4x4 numpy.array
    :rtype: 3x3 numpy.array
    """
    s = transform.shape
    if s[0] != s[1]:
        raise ValueError('Matrix must be a 4x4 homogenous transformation', s)
    n = s[0]
    rotation = transform[0:n - 1, 0:n - 1]
    return rotation


def create_homogeneous_transform_from_point(p):
    """
    Create a homogeneous transform to move to a given point
    :param p: The point we want our homogeneous transfrom to move to
    :type p: 1x3 numpy.array
    :rtype: 4x4 numpy.array
    """
    I = np.identity(3)
    T = np.vstack((I, np.zeros((3,))))
    p = np.hstack((p, np.ones(1))).reshape((4, 1))
    T = np.hstack((T, p))
    return T


def create_point_from_homogeneous_transform(T):
    """
    Create a point from a homogeneous transform
    :param T: The homogeneous transform
    :type T: 4x4 numpy.array
    :rtype: 1x3 numpy.array
    """
    return T[0:3, 3]
