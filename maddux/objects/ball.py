"""
A ball object to throw.
"""
import numpy as np
from throwable import ThrowableObject


class Ball(ThrowableObject):

    def __init__(self, position, radius):
        self.radius = radius
        self.name = "ball"
        ThrowableObject.__init__(self, position)

    
