"""
A base throwable object class that encodes traits like gravity,
velocity, etc.
"""
import numpy as np
from dynamic import DynamicObject

GRAVITY = -9.81
TIME = 0.001


class ThrowableObject(DynamicObject):

    def __init__(self, position):
        """Throwable Object Init"""
        self.attached = True
        self.velocity = np.array([0, 0, 0])
        DynamicObject.__init__(self, position)

    def throw(self, velocity):
        """Throw an object.
        :param velocity: 1x3 numpy array of object velocities
        """
        self.attached = False
        self.velocity = np.array(velocity)

    def step(self):
        """Update one timestep (one ms)"""
        if not self.attached:
            self.velocity[2] += TIME * GRAVITY
            self.position += TIME * self.velocity
            self.positions = np.vstack((self.positions,
                                        self.position.copy()))

    def attach(self):
        self.attached = True
        self.velocity = np.array([0, 0, 0])

    def display(self):
        print "Positon: {}".format(self.position)
        print "Velocity: {}".format(self.velocity)
        print "Attached: {}".format(self.attached)
