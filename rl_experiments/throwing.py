import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from maddux.robots import simple_human_arm
from maddux.environment import Environment
from maddux.objects import Target, Ball
import numpy as np

ACCEL_CHANGE = 0.1
TIME = 0.1


class ThrowingArm(object):

    actions = []

    def __init__(self, num_joints):
        self.actions = [-1, 1] * num_joints
        self.actions += ["Throw"]
        self.collected_rewards = []
        self.released = False

        self.ball = Ball(np.array([0, 0, 0]), 0.15)
        self.target = Target(np.array([2.0, 10.0, 2.0]), 0.5)

        q = np.array([0, 0, 0, np.pi / 2, 0, 0, 0])
        self.robot = simple_human_arm(1.0, 1.0, q, np.array([2.0, 2.0, 2.0]))

        room_dimensions = np.array([10.0, 10.0, 20.0])
        self.env = Environment(room_dimensions,
                               dynamic_objects=[ball],
                               static_objects=[target],
                               robot=self.robot)

        self.max_distance = np.linalg.norm(room_dimensions)

    def observe(self):
        """Returns current observation"""
        joint_velocities = [link.velocity for link in self.links]
        joint_angles = [link.theta for link in self.links]
        return joint_velocities + joint_angles

    def perform_action(self, action):
        """Update internal state to reflect the fact that an action was taken
        :param action: Number of the action performed
        """
        if action < 8:
            # Update a specific links velocity
            link = action / 2

            # TODO: Colin, what arm joints do we actually want to update? Is it first 4?
            self.robot.update_link_velocity(link, ACCEL_CHANGE * self.actions[action],
                                            TIME)
        else:
            # Or release the ball
            self.robot.release()
            self.released = True

    def step(self, dt):
        """Update internal state as if time dt has passed"""
        pass
    
    def is_over(self):
        """Check if simulation is over"""
        return self.released

    def collect_reward(self, action):
        """Returns reward accumulated since last time this function was called"""
        # Get previous landing position
        prior_landing_pos = self.env.hypothetical_landing_position()

        # Then perform the action and get new landing position
        self.perform_action(action)
        new_landing_pos = self.env.hypothetical_landing_position()

        if action == "Throw":
            # If we threw it, see the distance
            reward = self.max_distance - new_landing_pos
        else:
            # Otherwise, see how much we improved
            reward = new_landing_pos - prior_landing_pos
        self.collected_rewards.append(reward)
        return reward
