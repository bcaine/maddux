"""
Simulation to teach robot how to throw a ball.
DOES NOT CURRENTLY WORK!
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from maddux.robots import simple_human_arm
from maddux.environment import Environment
from maddux.objects import Target, Ball
import numpy as np

ACCEL_CHANGE = 2.0
TIME = 0.1


class ThrowingArm(object):

    actions = []

    def __init__(self, num_joints=4):
        self.actions = [-1, 1] * num_joints
        self.actions += ["Throw"]
        self.move_count = 0
        self.collected_rewards = []
        self.released = False
        self.num_actions = len(self.actions)
        self.observation_size = len(self.actions)


        self.ball = Ball(np.array([0, 0, 0]), 0.15)
        self.target = Target(np.array([2.0, 10.0, 2.0]), 0.5)

        q = np.array([0, 0, 0, np.pi / 2, 0, 0, 0])
        self.robot = simple_human_arm(1.0, 1.0, q, np.array([2.0, 2.0, 2.0]))

        room_dimensions = np.array([10.0, 10.0, 20.0])
        self.env = Environment(room_dimensions,
                               dynamic_objects=[self.ball],
                               static_objects=[self.target],
                               robot=self.robot)

        self.max_distance = np.linalg.norm(room_dimensions)
        self.distance_to_target = self.max_distance

    def observe(self):
        """Returns current observation"""
        landing_positions = []
        for i, action in enumerate(self.actions):
            if action == "Throw":
                landing_pos = self.env.hypothetical_landing_position()
            else:
                link = i / 2
                # Perform link update
                self.robot.update_link_velocity(link, ACCEL_CHANGE *\
                                                self.actions[i], TIME)
                # Calculate hypothetical landing spot as observation
                landing_pos = self.env.hypothetical_landing_position()

                # Undo link update
                self.robot.update_link_velocity(link, -ACCEL_CHANGE *\
                                                self.actions[i], TIME)

            distance = np.linalg.norm(landing_pos - self.target.position)
            landing_positions.append(distance)
        return np.array(landing_positions)

    def perform_action(self, action):
        """Update internal state to reflect the fact that an action was taken
        :param action: Number of the action performed
        """
        if action < 8:
            # Update a specific links velocity
            link = action / 2
            self.robot.update_link_velocity(link, ACCEL_CHANGE *\
                                            self.actions[action], TIME)
            self.move_count += 1
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
        """Returns reward accumulated since last time this
        function was called.
        """
        # Get previous landing position
        prior_landing_pos = self.env.hypothetical_landing_position()

        prior_dist = np.linalg.norm(self.target.position - prior_landing_pos)

        # Then perform the action and get new landing position
        self.perform_action(action)
        new_landing_pos = self.env.hypothetical_landing_position()
        new_dist = np.linalg.norm(self.target.position - new_landing_pos)

        if self.actions[action] == "Throw":
            # If we threw it, see the distance
            reward = -new_dist + 1.0
        else:
            # Otherwise, see how much we improved
            reward = (prior_dist - new_dist)

        self.distance_to_target = new_dist
        self.collected_rewards.append(reward)
        return reward

    def display_actions(self):
        print "Moved {} times before throwing!".format(self.move_count)
        print "Last reward: {}".format(self.collected_rewards[-1])

