"""
Planning done with a much simpler reward.
Takes a long time to converge as untill the arm finds
the target it is operating at random.
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import numpy as np
from maddux.rl_experiments.planning import Planning

class SimpleRewardPlanning(Planning):

    def __init__(self, environment, change_per_iter=0.1, target_accuracy=0.25):
        Planning.__init__(self, environment, change_per_iter, target_accuracy)

    def is_over(self):
        """Check if simulation is over"""
        if self.collected_rewards and self.collected_rewards[-1] == -100:
            return True

        target = self.target.position
        end_effector = self.robot.end_effector_position()
        return np.linalg.norm(target - end_effector) < self.target_accuracy

    def collect_reward(self, action):
        """Returns reward accumulated since last time this
        function was called.
        """
        self.perform_action(action)
        for obstacle in self.static_objects:
            if self.robot.is_in_collision(obstacle):
                self.collected_rewards.append(-100)
                return -100

        target = self.target.position
        end_effector = self.robot.end_effector_position()
        if np.linalg.norm(target - end_effector) < self.target_accuracy:
            self.collected_rewards.append(100)
            return 100

        self.collected_rewards.append(-0.01)
        return -0.1

