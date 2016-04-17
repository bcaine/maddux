import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from maddux.robots import simple_human_arm
from maddux.environment import Environment
from maddux.objects import Ball, Obstacle
import numpy as np

POS_CHANGE = 0.1
ACCURACY = 0.05

class HardPlanning(object):

    def __init__(self, num_joints=4):
        self.actions = [-1, 1] * num_joints
        self.move_count = 0
        self.collected_rewards = []
        self.num_actions = len(self.actions)
        self.observation_size = len(self.actions)

        obs_front = Obstacle([0.0, 2.0, 0.0], [1.5, 2.5, 3.0])
        obs_back = Obstacle([0.0, 4.0, 0.0], [1.5, 4.5, 3.0])
        obs_left = Obstacle([0.0, 2.5, 0.0], [0.5, 4.0, 3.0])
        obs_top = Obstacle([0.0, 2.0, 3.0], [1.5, 4.5, 3.5])
        obs_bottom = Obstacle([0.5, 2.5, 0.0], [1.5, 4.0, 1.0])
        self.obstacles = [obs_front, obs_back, obs_left, obs_top, obs_bottom]

        self.ball = Ball([1.0, 3.25, 2.0], 0.5)

        q = np.array([0, 0, 0, -np.pi/2.0, 0, 0, 0])
        self.robot = simple_human_arm(3.0, 2.0, q, np.array([1.0, 1.0, 0.0]))

        room_dimensions = np.array([10.0, 10.0, 20.0])
        self.env = Environment(room_dimensions,
                               dynamic_objects=[self.ball],
                               static_objects=self.obstacles,
                               robot=self.robot)
        self.env.plot()

    def observe(self):
        """Returns current observation"""
        distances = []
        for i, action in enumerate(self.actions):
            link = i / 2

            # Calculate old and new link positions
            q_old = self.robot.links[link].theta
            q_new = q_old + action * POS_CHANGE

            # Get the end effector position after joint rotation
            current_config = self.robot.get_current_joint_config()
            current_config[link] = q_new
            end_effector_pos = self.robot.end_effector_position(current_config)

            # Find the distance from our target (the ball)
            distance = np.linalg.norm(end_effector_pos -\
                                      self.ball.position)
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
        q_new = q_old + self.actions[action] * POS_CHANGE

        self.robot.update_link_angle(link, q_new, save=True)
        self.move_count += 1

    def is_over(self):
        """Check if simulation is over"""
        for obstacle in self.obstacles:
            if self.robot.is_in_collision(obstacle):
                return True

        target = self.ball.position
        end_effector = self.robot.end_effector_position()
        return np.linalg.norm(target - end_effector) < ACCURACY

    def collect_reward(self, action):
        """Returns reward accumulated since last time this
        function was called.
        """
        # Calculate previous distance to target object (ball)
        old_dist = np.linalg.norm((self.robot.end_effector_position() -
                                   self.ball.position))
        # Then perform the action
        self.perform_action(action)

        for obstacle in self.obstacles:
            if self.robot.is_in_collision(obstacle):
                self.collected_rewards.append(-1)
                return -1

        # Find the distance from our target (the ball)
        new_dist = np.linalg.norm((self.robot.end_effector_position() -
                                   self.ball.position))
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


