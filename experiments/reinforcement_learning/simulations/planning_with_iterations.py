import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import numpy as np

class Planning(object):

    def __init__(self, environment, change_per_iter=0.1, target_accuracy=0.25, max_iterations=500):
        """
        Planning module to take an environment and run RL experiments on
        :param environment: Environment containing robot, obstacles, target, etc.
        :type environment: maddux.Environment
        :param change_per_iter: Change of a joint config each action in radians
        :type change_per_iter: integer
        :param target_accuracy: Accuracy needed to declare target hit
        :type target_accuracy: integer
        :rtype: None
        """
        self.change_per_iter = change_per_iter
        self.target_accuracy = target_accuracy
        self.static_objects = environment.static_objects
        self.dynamic_objects = environment.dynamic_objects
        self.robot = environment.robot
        self.env = environment
        self.max_iterations = max_iterations
        self.iterations = 0

        # TODO: This is a dumb assumption, make it better
        # Assume target is first dynamic object
        self.target = self.dynamic_objects[0]

        # Define our actions and observation data
        self.actions = [-1, 1] * self.robot.active_links
        self.move_count = 0
        self.collected_rewards = []
        self.num_actions = len(self.actions)
        self.observation_size = 5

        self.hit_obstacle = False
        self.reached_max_iterations = False
        self.hit_target = False

    def observe(self):
        """
        Returns current observation
        :rtype: 1x4 numpy.array
        """
        iteration_factor = self.iterations / (self.max_iterations / 4)
        return np.append(self.robot.get_current_joint_config()[0:4], iteration_factor)

    def perform_action(self, action):
        """
        Update internal state to reflect the fact that an action was taken
        :param action: Number of the action performed
        :type action: integer
        :rtype: None
        """
        # Update a specific links velocity
        link = action / 2
        q_old = self.robot.links[link].theta
        q_new = q_old + self.actions[action] * self.change_per_iter

        self.robot.update_link_angle(link, q_new, True)
        self.move_count += 1

    def is_over(self):
        """
        Check if simulation is over
        :rtype: Boolean
        """
        if self.hit_obstacle or self.reached_max_iterations or self.hit_target:
            return True

        self.iterations += 1

    def collect_reward(self, action):
        """
        Returns reward accumulated since last time this function was called.
        :param action: The action preformed
        :type action: integer
        :rtype: integer
        """
        reward = 0
        if self.iterations == self.max_iterations:
            self.reached_max_iterations = True
            return -1000

        iteration_factor = self.iterations / (self.max_iterations / 4)
        if iteration_factor == 4:
            reward -= 5
        elif iteration_factor == 3:
            reward -= 3
        elif iteration_factor == 2:
            reward -= 2
        elif iteration_factor == 1:
            reward -= 1

        # Calculate previous distance to target object (ball)
        old_dist = np.linalg.norm((self.robot.end_effector_position() -
                                   self.target.position))
        # Then perform the action
        self.perform_action(action)

        for obstacle in self.static_objects:
            if self.robot.is_in_collision(obstacle):
                self.hit_obstacle = True
                self.collected_rewards.append(-100)
                return reward-1000

        # Find the distance from our target (the ball)
        new_dist = np.linalg.norm((self.robot.end_effector_position() -
                                   self.target.position))

        # If we hit the target, give it a big reward
        if new_dist < self.target_accuracy:
            self.hit_target = True
            reward += 1000
        else:
            # Reward it if it decreased the distance between end effector
            # and target (ball).
            dis_diff = old_dist - new_dist
            if dis_diff > 0:
                reward += dis_diff * 2
            else:
                reward += dis_diff

        self.collected_rewards.append(reward)
        return reward

    def display_actions(self):
        """
        Displays planning properties
        :rtype: None
        """
        print "Last reward: {}".format(self.collected_rewards[-1])

    def save_path(self, filepath, iteration):
        """
        Saves the current robot joint config to a file
        :param filepath: The directory to save the config to
        :type filepath: String
        :param iteration: The current simulation iteration
        :type iteration: integer
        :rtpye: None
        """
        filename = "{}/planning_path_{}".format(filepath, iteration)
        np.save(filename, self.robot.qs)
