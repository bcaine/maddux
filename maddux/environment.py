"""
Our experiment environment.
"""
import numpy as np
from objects import Ball, Target

class Environment:

    def __init__(self, dimensions):
        """
        Our room goes from [0, 0, 0] to [x, y, z]
        :param dimensions: 1x3 array of the dimensions of the room.
        """
        self.dimensions = dimensions
        self.objects = []
        

    def add_object(self, obj):
        """
        :param obj: An object (like a ball, robot, or target) to add
                    to the environment.
        """
        self.objects.append(obj)


    def run(self, duration):
        """Run for a certain duration
        :param duration: duration to run environment in ms
        """

        for _ in xrange(duration):
            for obj in self.objects:
                obj.step()

