"""
An abstract base class for dynamic objects.
"""
import abc
import numpy as np

class DynamicObject:
    __metaclass__ = abc.ABCMeta

    def __init__(self, position):
        self.position = np.array(position)
        self.positions = np.array([self.position.copy()])

    @abc.abstractmethod
    def step(self):
        """Step forward in time (one ms)"""
        return

    @abc.abstractmethod
    def attach(self):
        """Attach to an object (stop moving)"""
        return

    @abc.abstractmethod
    def display(self):
        """Display information"""
        return

    @abc.abstractmethod
    def leading_point(self):
        """Returns position of leading point in the direction the object
           is traveling.
        """
        return

    @abc.abstractmethod
    def plot(self, ax):
        """Plot the dynamic object at its current location"""
        return
