"""
A robot arm defined by a sequence of DH links
"""
import numpy as np
import utils

class Arm:

    # TODO: Do something about active_links, its real bad...
    # TODO: Make sure the tool frame works
    def __init__(self, links, q0, name, active_links=None, base=None, tool=None):
        """A robotic arm.
        :param links: Vector of Link objects
        :type links: 1xN numpy.array
        :param q0: The default (resting state) joint configuration
        :type q0: 1xN numpy.array
        :param name: Name of the arm
        :type name: String
        :param active_links: Number of active links on the arm (Defaults to all)
        :type active_links: integer or None
        :param base: Base position of the arm in (x,y,z) cords
        :type base: 1x3 numpy.array or None
        :param tool: Tool location in (z,y,z) cords
        :type tool: 1x3 numpy.array or None
        :rtype: None
        """
        self.num_links = links.size
        self.links = links
        self.q0 = q0
        self.name = name

        if active_links is None:
            self.active_links = len(links)
        else:
            self.active_links = active_links

        if base is None:
            self.base = np.identity(4)
        else:
            self.base = utils.create_homogeneous_transform_from_point(base)

        if tool is None:
            self.tool = np.identity(4)
        else:
            self.tool = utils.create_homogeneous_transform_from_point(tool)

        # Create empty list of held objects
        self.held_objects = []

        # A cache of all past q values for a run of ikine so we
        # can animate the action
        self.qs = np.array([q0.copy()])

        # Set the arm to its default position
        self.reset()

    def reset(self):
        """
        Resets the arm back to its resting state, i.e. q0
        :rtype: None
        """
        self.update_angles(self.q0)

    def get_current_joint_config(self):
        """
        Gets the current joint configuration from the links
        :rtype: 1xN numpy.array
        """
        q = np.zeros(self.num_links)
        for i, link in enumerate(self.links):
            q[i] = link.theta
        return q

    def update_angles(self, new_angles):
        """
        Updates all the link's angles
        :param new_angles: The new link angles
        :type new_angles: 1xN numpy.array
        :rtype: None
        """
        for link, new_theta in zip(self.links, new_angles):
            link.set_theta(new_theta)
        self.update_link_positions()

    def update_link_angle(self, link, new_angle, save=False):
        """
        Updates the given link's angle with the given angle
        :param link: The link you want to update
        :type link: integer
        :param new_angle: The link's new angle
        :type new_angle: integer
        :paran save: Flag that determines if the update is cached
        :type Boolean
        :rtype: None
        """
        self.links[link].set_theta(new_angle)
        self.update_link_positions()

        # Save each config for replay
        if save:
            q = np.array([l.theta for l in self.links])
            self.qs = np.vstack((self.qs, q.copy()))

    # TODO: Acceleration over time seems like a weird way to update this
    def update_link_velocity(self, link, accel, time):
        """
        Updates the given link's velocity with the given
        acceleration over the given time
        :param link: The link you want to update
        :type link: integer
        :param accel: The acceleration (Radians per second^2)
        :type accel: integer
        :param time: The time (Seconds)
        :type time: integer
        :rtype: None
        """
        self.links[link].update_velocity(accel, time)
        self.update_link_positions()

    def update_link_positions(self):
        """
        Walk through all the links and update their positions.
        :rtype: None
        """

        for i, link in enumerate(self.links):
            # Set link base position
            if i == 0:
                link.base_pos = utils.create_point_from_homogeneous_transform(
                    self.base)
            else:
                link.base_pos = self.links[i - 1].end_pos

            # Set link end position
            if link.length == 0 and link.offset == 0:
                link.end_pos = link.base_pos
            else:
                # Compute FKine up to that link endpoint
                # to get the location in homogenous coords
                t = self.fkine(links=range(i + 1))
                # Then convert that to world space
                end_pos = utils.create_point_from_homogeneous_transform(t).T
                link.end_pos = end_pos.A1

        # After we update all these link positions, we can update
        # the location of any object we are holding
        for held_object in self.held_objects:
            held_object.position = self.end_effector_position()

    def end_effector_position(self, q=None):
        """
        Return end effector position
        :param q: Config to compute the end effector position on
        :type q: 1xN numpy.array or None
        :rtype: 1x3 numpy.array
        """
        if q is None:
            return self.links[-1].end_pos

        t = self.fkine(q=q)
        end_pos = utils.create_point_from_homogeneous_transform(t).T
        return end_pos

    def end_effector_velocity(self):
        """
        Calculate the end effector velocity of the arm given
        its current angular velocities.
        :rtype: integer
        """
        q = np.array([link.theta for link in self.links])
        dq = np.array([link.velocity for link in self.links])

        velocity = self.jacob0(q) * np.asmatrix(dq).T
        return velocity.A1


    def fkine(self, q=None, links=None):
        """
        Computes the forward kinematics of the arm using the current joint
        configuration or a given joint configuration
        :param q: (Optional) joint configuration to compute the FK on
        :type q: 1xN numpy.array or None
        :param links: (Optional) Specify which links to run fkine on
        :type links: integer or None
        :rtype: 4x4 numpy.array
        """
        if links is None:
            links = range(self.num_links)

        t = self.base
        # TODO: Whats the point of links? Seems unused/used wrong
        for i, link in zip(links, self.links):
            if np.any(q):
                t = t * link.compute_transformation_matrix(q[i])
            else:
                t = t * link.transform_matrix
        t = t * self.tool
        return t

    def ikine(self, p, num_iterations=1000, alpha=0.1):
        """
        Computes the inverse kinematics to find the correct joint
        configuration to reach a given point
        :param p: The point we want to solve the inverse kinematics for
        :type p: 1x3 numpy.array
        :param num_iterations: The number of iterations to try before
                               giving up
        :type num_iterations: integer
        :param alpha: The stepsize for the ikine solver (0.0 - 1.0)
        :type alpha: integer
        :rtype: 1xN numpy.array
        """
        # Check to make sure alpha is between 0 and 1
        if not (0.0 <= alpha <= 1.0):
          print "Invalid alpha. Defaulting to 0.1"
          alpha = 0.1

        q = self.get_current_joint_config()
        self.qs = np.array([q.copy()])

        goal = utils.create_homogeneous_transform_from_point(p)
        for i in xrange(num_iterations):
            # Calculate position error of the end effector
            curr = self.fkine(q)
            err = goal - curr

            # Convert error from homogeneous to xyz space
            err = utils.create_point_from_homogeneous_transform(err)

            # Get the psudoinverse of the Jacobian
            J = self.jacob0(q)
            vel_J = J[0:3, :]

            # Increment q a tiny bit
            delta_q = np.linalg.pinv(vel_J) * err
            delta_q = np.squeeze(np.asarray(delta_q))
            q = q + (alpha * delta_q.flatten())
            self.qs = np.vstack((self.qs, q.copy()))

            if abs(np.linalg.norm(err)) <= 1e-6:
                return q
        raise ValueError("Could not find solution.")

    def jacob0(self, q=None):
        """
        Calculates the jacobian in the world frame by finding it in
        the tool frame and then converting to the world frame
        :param q: Optional joint configuration to compute the jacobian on
        :type q: 1xN numpy.array
        :rtype: 6xN numpy.array
        """

        # Get the tool frame jacobian
        J = self.jacobn(q)

        # Set up homogeneous transform matrix for the world
        eet = self.fkine(q)
        rotation = utils.get_rotation_from_homogeneous_transform(eet)
        zeros = np.zeros((3, 3))
        a1 = np.hstack((rotation, zeros))
        a2 = np.hstack((zeros, rotation))

        # Convert to world frame
        J = np.vstack((a1, a2)) * J
        return J

    def jacobn(self, q=None):
        """
        Calculates the jacobian in the tool frame
        :param q: Optional joint configuration to compute the jacobian on
        :type q: 1xN numpy.array
        :rtype: 6xN numpy.array
        """
        J = np.zeros((6, self.num_links))
        U = self.tool
        I = range(self.num_links - 1, -1, -1)

        for i, link in zip(I, self.links[::-1]):
            if np.any(q):
                U = link.compute_transformation_matrix(q[i]) * U
            else:
                U = link.transform_matrix * U

            d = np.array([-U[0, 0] * U[1, 3] + U[1, 0] * U[0, 3],
                          -U[0, 1] * U[1, 3] + U[1, 1] * U[0, 3],
                          -U[0, 2] * U[1, 3] + U[1, 2] * U[0, 3]])
            delta = U[2, 0:3]

            J[:, i] = np.vstack((d, delta)).flatten()
        return J

    def hold(self, obj):
        """
        Hold a specific object
        :param obj: Object to be held
        :type obj: maddux.objects.DynamicObject
        :rtype: None
        """
        obj.attach()
        obj.position = self.end_effector_position()
        self.held_objects.append(obj)

    def release(self, object_idx=None):
        """Release one or all currently held objects
        :param object_idx: (Optional) index of object to release
        :type object_idx = integer or None
        :rtype: None
        """
        velocity = self.end_effector_velocity()[0:3]
        if object_idx is None:
            # Release all objects
            for obj in self.held_objects:
                obj.throw(velocity)
        else:
            # TODO: Replease with End Effector Velocity
            self.held_objects[object_idx].throw(velocity)


    # TODO: Let env_object be any object, not just static
    def is_in_collision(self, env_object):
        """
        Checks if the arm is in collision with a given object
        :param env_object: The object to check for collisions with
        :type env_object: maddux.Objects.StaticObject
        :rtype: Boolean
        """
        for link in self.links:
            if link.is_in_collision(env_object):
                return True
        return False

    def plot(self, ax):
        """Plot our robot into given axes
        :param ax: axes of plot
        :type ax: matplotlib figure
        :rtype: None
        """
        for link in self.links:
            link.plot(ax)
