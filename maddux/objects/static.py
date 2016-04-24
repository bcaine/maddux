"""
An abstract base class for static objects.
"""
import abc
import numpy as np


class StaticObject:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def is_hit(self, position):
        """Tells whether another object hit the static object"""
        return

    @abc.abstractmethod
    def display(self):
        """Display relevant data about static object."""
        return

    @abc.abstractmethod
    def plot(self, ax):
        """Plot static object."""
        return
