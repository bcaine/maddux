"""
A base throwable object class that encodes traits like gravity,
velocity, etc.
"""
import numpy as np
from maddux.objects.dynamic import DynamicObject

GRAVITY = -9.81
TIME = 0.001


class ThrowableObject(DynamicObject):

    def __init__(self, position, target=False):
        """Throwable Object Init"""
        self.attached = True
        self.target = target
        self.velocity = np.array([0, 0, 0])
        DynamicObject.__init__(self, position, target)

    def throw(self, velocity):
        """Throw an object.

        :param velocity: Velocity to throw at (vx, vy, vz)
        :type velocity: np.ndarray

        :rtype: None
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
        """Attach an object to its current position"""
        self.attached = True
        self.velocity = np.array([0, 0, 0])

    def display(self):
        """Display information about object"""
        print("Positon: {}".format(self.position))
        print("Velocity: {}".format(self.velocity))
        print("Attached: {}".format(self.attached))
