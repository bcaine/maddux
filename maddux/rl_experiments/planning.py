import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import numpy as np
from random import gauss


class Planning(object):

    def __init__(self, environment, change_per_iter=0.1, target_accuracy=0.25):
        """Planning module to take an environment and run RL experiments on
        :param environment: Environment containing robot, obstacles,
                            target etc.
        :param change_per_iter: Change of a joint each action
        :param target_accuracy: Accuracy needed to declare target hit
        """
        self.change_per_iter = change_per_iter
        self.target_accuracy = target_accuracy
        self.static_objects = environment.static_objects
        self.dynamic_objects = environment.dynamic_objects
        self.robot = environment.robot
        self.env = environment

        # Assume target is first dynamic object
        self.target = self.dynamic_objects[0]

        # Define our actions and observation data
        self.actions = [-1, 1] * self.robot.active_links
        self.move_count = 0
        self.collected_rewards = []
        self.num_actions = len(self.actions)
        self.observation_size = len(self.actions)

    def observe(self):
        """Returns current observation"""
        distances = []
        for i, action in enumerate(self.actions):
            link = i / 2

            # Calculate old and new link positions
            q_old = self.robot.links[link].theta
            q_new = q_old + action * self.change_per_iter

            # Get the end effector position after joint rotation
            current_config = self.robot.get_current_joint_config()
            current_config[link] = q_new
            end_effector_pos = self.robot.end_effector_position(
                current_config)

            # Find the distance from our target (the ball)
            distance = np.linalg.norm(end_effector_pos - self.target.position)
            # Distances + some noise
            distances.append(distance)
        return np.array(distances)

    def perform_action(self, action):
        """Update internal state to reflect the fact that an
           action was taken
        :param action: Number of the action performed
        """
        # Update a specific links velocity
        link = action / 2
        q_old = self.robot.links[link].theta
        q_new = q_old + self.actions[action] * self.change_per_iter

        self.robot.update_link_angle(link, q_new, True)
        self.move_count += 1

    def is_over(self):
        """Check if simulation is over"""
        if self.collected_rewards and self.collected_rewards[-1] == -1:
            return True

        target = self.target.position
        end_effector = self.robot.end_effector_position()
        return np.linalg.norm(target - end_effector) < self.target_accuracy

    def collect_reward(self, action):
        """Returns reward accumulated since last time this
        function was called.
        """
        # Calculate previous distance to target object (ball)
        old_dist = np.linalg.norm((self.robot.end_effector_position() -
                                   self.target.position))
        # Then perform the action
        self.perform_action(action)

        for obstacle in self.static_objects:
            if self.robot.is_in_collision(obstacle):
                self.collected_rewards.append(-1)
                return -1

        # Find the distance from our target (the ball)
        new_dist = np.linalg.norm((self.robot.end_effector_position() -
                                   self.target.position))

        # If we hit the target, give it a big reward
        if new_dist < self.target_accuracy:
            reward = 10
        else:
            # Reward it if it decreased the distance between end effector
            # and target (ball).
            reward = old_dist - new_dist
            if reward > 0:
                reward *= 2
        self.collected_rewards.append(reward)
        return reward

    def display_actions(self):
        print "Moved {} times before throwing!".format(self.move_count)
        print "Last reward: {}".format(self.collected_rewards[-1])

    def save_path(self, filepath, iteration):
        filename = "{}/planning_path_{}".format(filepath, iteration)
        np.save(filename, self.robot.qs)


