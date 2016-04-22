"""
An abstract base class for dynamic objects.
"""
import abc
import numpy as np


class DynamicObject:
    __metaclass__ = abc.ABCMeta

    def __init__(self, position, target=False):
        """DynamicObject abstract class init

        :param position: Current (x,y,z) position of the Dynamic Object
        :type position: numpy.ndarray

        :param target: (Default=False) Whether this object is the target of
                       an experiment
        :type target: bool
        """
        self.position = np.array(position)
        self.target = target
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
    def plot(self, ax):
        """Plot the dynamic object at its current location"""
        return
