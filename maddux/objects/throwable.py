"""
A base throwable object class that encodes traits like gravity,
velocity, etc.
"""
import numpy as np

GRAVITY=-9.81

class ThrowableObject:

    def __init__(self, position):
        """Throwable Object Init"""
        self.position = position


    def throw(self, velocity):
        """Throw an object.
        
        :param velocity: 1x3 numpy array of object velocities
        """
        self.velocity = velocity

    def step(self, time_ms):
        """Step through time
        
        :param time_ms: Float - Time in Milliseconds
        """

        # TODO: Add check for intersecting environment?
        # Or maybe we want to do that outside of this fn
        for _ in xrange(time_ms):
            self.position += 0.001 * self.velocity
        
