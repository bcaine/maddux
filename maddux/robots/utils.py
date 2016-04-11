"""
Random collection of utilities for the robots to use
"""

import numpy as np

def get_rotation_from_homogenous_transform(transform):
    """
    Extract the rotation section of the homogenous transformation
    :param transform: The homogenous transform to extract the rotation matrix from
    """
    s = transform.shape
    if s[0] != s[1]:
      raise ValueError('Matrix must be a 4x4 homogenous transformation', s)
    n = s[0]
    rotation = transform[0:n-1, 0:n-1]
    return rotation
