"""
A Link in a robot arm.
"""
import numpy as np


class Link:

    def __init__(self, length, q, position):
        """
        :param length: Length of arm segment
        :param q: Initial joint angles
        :param position: Location of arm (at base)
        """
        self.length = length
        self.q = q
        self.position = position

    def update(self, new_q):
        """Update the arm angles"""
        self.q = new_q


    
