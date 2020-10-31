"""
A Link object holds all information related to a robot link such as
the DH parameters and position in relation to the world.
"""
import numpy as np
from maddux.plot import plot_sphere
import math


class Link:

    def __init__(self, theta, offset, length, twist,
                 q_lim=None, max_velocity=30.0, link_size=0.1,
                 connector_size=0.1):
        """Link init

        :param theta: Link angle, variable
        :type theta: int

        :param offset: Link offset, constant
        :type offset: int

        :param length: Link length, constant
        :type length: int

        :param twist: Link twist, constant
        :type twist: int

        :param q_lim: Joint coordinate limits
        :type q_lim: numpy.ndarray or None

        :param max_velocity: Maximum radians the link can rotate per second
        :type max_velocity: int

        :param link_size: The size of the link (used in collision detection
                          and plotting)
        :type link_size: int

        :param connector_size: The size of the link connector
        :type  connector_size: int

        :rtype: None
        """
        self.offset = offset
        self.length = length
        self.twist = twist
        self.q_lim = q_lim

        self.max_velocity = max_velocity
        self.link_size = link_size
        self.connector_size = connector_size

        self.set_theta(theta)
        self.velocity = 0  # Link's current velocity

        # This is updated once we add it to an arm
        self.base_pos = None
        self.end_pos = None

    def set_theta(self, theta):
        """Sets theta to the new theta and computes the new
        transformation matrix

        :param theta: The new theta for the link
        :type theta: int

        :rtype: None
        """
        self.theta = theta
        self.transform_matrix = self.compute_transformation_matrix(theta)

    def update_velocity(self, accel, time):
        """Updates the current velocity of the link when acted upon
        by some acceleration over some time

        :param accel: The acceleration acting upon the link
                      (radians per second^2)
        :type accel: int

        :param time: The time the accelration is applied over (seconds)
        :type time: int

        :rtype: None
        """
        new_velocity = self.velocity + (accel * time)
        if new_velocity <= self.max_velocity:
            self.velocity = new_velocity
            new_theta = self.theta + (new_velocity * time)
            new_theta = math.atan2(math.sin(new_theta),
                                   math.cos(new_theta))
            self.set_theta(new_theta)

    def compute_transformation_matrix(self, q):
        """Transformation matrix from the current theta to the new theta

        :param q: the new theta
        :type q: int

        :returns: Transformation matrix from current q to provided q
        :rtype: 4x4 numpy matrix
        """
        sa = np.sin(self.twist)
        ca = np.cos(self.twist)
        st = np.sin(q)
        ct = np.cos(q)
        T = np.matrix([[ct, -st * ca, st * sa, self.length * ct],
                       [st, ct * ca, -ct * sa, self.length * st],
                       [0, sa, ca, self.offset],
                       [0, 0, 0, 1]])
        return T

    # TODO: Abstract this to take dynamic objects as well as static ones
    def is_in_collision(self, env_object):
        """Checks if the arm is in collision with a given static object

        :param env_object: The object to check for collisions with
        :type env_object: maddux.objects.StaticObject

        :returns: Whether link hits the provided env_object
        :rtype: bool
        """
        intersects_joint = env_object.is_hit_by_sphere(self.base_pos,
                                                       self.link_size)
        # If the link sphere is in collision we do not need to
        # check anything else
        if intersects_joint:
            return True

        # If the link is just a joint we only needed to check sphere,
        # and since we would have already returned, we know we're safe
        if self.length == 0 and self.offset == 0:
            return False

        # Otherwise we need to check if the object intersects with
        # the arm connector, so we vectorize it and call is_hit
        lamb = np.linspace(0, 1, 100)
        v = self.end_pos - self.base_pos

        positions = self.base_pos + lamb[:, np.newaxis] * v

        return env_object.is_hit(positions)

    def display(self):
        """Display the link's properties nicely

        :rtype: None
        """
        print('Link angle: {}'.format(self.theta))
        print('Link offset: {}'.format(self.offset))
        print('Link length: {}'.format(self.length))
        print('Link twist: {}'.format(self.twist))

    def plot(self, ax):
        """Plots the link on the given matplotlib figure

        :param ax: Figure to plot link upon
        :type ax: matplotlib.axes

        :rtype: None
        """
        if self.base_pos is None or self.end_pos is None:
            raise ValueError("Base and End positions were never defined")

        plot_sphere(self.end_pos, self.link_size, ax, color='black')

        # If there's no length associated, we don't have to draw one
        if self.length == 0 and self.offset == 0:
            return ax

        pts = np.vstack((self.base_pos, self.end_pos))

        return ax.plot(pts[:, 0], pts[:, 1], pts[:, 2],
                       color='b', linewidth=3)
