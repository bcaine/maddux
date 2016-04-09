"""
A ball object to throw.
"""
import numpy as np
from throwable import ThrowableObject


class Ball(ThrowableObject):

    def __init__(self, position, radius):
        self.radius = radius
        ThrowableObject.__init__(self, position)

    
