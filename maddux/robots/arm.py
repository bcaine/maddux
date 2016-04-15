"""
A robot arm
"""
import numpy as np
import utils


class Arm:

    def __init__(self, links, q0, name, base=None, tool=None):
        """A robotic arm.
        :param links: Vector of Link objects (1xN numpy vector)
        :param q0: The default (resting state) joint configuration
                   (1xN numpy vector)
        :param name: Name of the arm
        :param base: Base position of the arm (1x3 numpy array)
        :param tool: Tool location.
        """
        self.num_links = links.size
        self.links = links
        self.q0 = q0
        self.name = name

        if base is None:
            self.base = np.identity(4)
        else:
            self.base = utils.create_homogeneous_transform_from_point(base)

        if tool is None:
            self.tool = np.identity(4)
        else:
            self.tool = tool

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
        """
        self.update_angles(self.q0)

    def update_angles(self, new_angles):
        """
        Updates all the link's angles
        :param new_angles: 1xN numpy array of link angles
        """
        for link, new_theta in zip(self.links, new_angles):
            link.set_theta(new_theta)
        self.update_link_positions()

    def update_link_angle(self, link, new_angle):
        """
        Updates the given link's angle with the given angle
        :param link: The link you want to update, given as a integer
        :param new_angle: The link's new angle
        """
        self.links[link].set_theta(new_angle)
        self.update_link_positions()

    def update_link_velocity(self, link, accel, time):
        """
        Updates the given link's velocity with the given
        acceleration over the given time
        :param link: The link you want to update, given as a integer
        :param accel: The acceleration (Radians per second^2)
        :param time: The time (Seconds)
        """
        self.links[link].update_velocity(accel, time)
        self.update_link_positions()

    def get_current_joint_config(self):
        """
        Gets the current joint configuration from the links
        """
        q = np.zeros(self.num_links)
        for i, link in enumerate(self.links):
            q[i] = link.theta
        return q

    def fkine(self, q=None, links=None):
        """
        Computes the forward kinematics of the arm using the current joint
        configuration or a given joint configuration
        :param q: (Optional) joint configuration to compute the FK on
                  (1xN numpy vector)
        :param links: (Optional) Specify which links to run fkine on
        """
        if links is None:
            links = range(self.num_links)

        t = self.base
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
        :param num_iterations: The number of iterations to try before
                               giving up
        :param alpha: The stepsize for the ikine solver
        """
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
                  (1xN numpy vector)
        """
        J = self.jacobn(q)
        eet = self.fkine(q)
        rotation = utils.get_rotation_from_homogeneous_transform(eet)
        zeros = np.zeros((3, 3))
        a1 = np.hstack((rotation, zeros))
        a2 = np.hstack((zeros, rotation))
        J = np.vstack((a1, a2)) * J
        return J

    def jacobn(self, q=None):
        """
        Calculates the jacobian in the tool frame
        :param q: Optional joint configuration to compute the jacobian on
                  (1xN numpy vector)
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

    def plot(self, ax):
        """Plot our robot
        :param ax: axes of plot
        """
        for link in self.links:
            link.plot(ax)

    def update_link_positions(self):
        """
        Walk through all the links and update their positions.
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

    def end_effector_position(self):
        """Return end effector position"""
        return self.links[-1].end_pos

    def hold(self, obj):
        """Hold a specific object"""
        obj.attach()
        obj.position = self.end_effector_position()
        self.held_objects.append(obj)

    def release(self, object_idx=None):
        """Release one or all currently held objects
        :param object_idx: (Optional) index of object to release
        """

        velocity = self.end_effector_velocity()[0:3]
        if object_idx is None:
            # Release all objects
            for obj in self.held_objects:
                obj.throw(velocity)
        else:
            # TODO: Replease with End Effector Velocity
            self.held_objects[object_idx].throw(velocity)

    def end_effector_velocity(self):
        """Calculate the end effector velocity of the arm given 
        its current angular velocities.
        """
        q = np.array([link.theta for link in self.links])
        dq = np.array([link.velocity for link in self.links])

        velocity = self.jacob0(q) * np.asmatrix(dq).T
        return velocity.A1


