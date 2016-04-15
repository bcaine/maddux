import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from maddux.robots import simple_human_arm
from maddux.environment import Environment
from maddux.objects import Target, Ball
import numpy as np


class ThrowingArm(object):

    actions = []

    def __init__(self, num_joints):
        self.actions = [-1, 1] * num_joints
        self.actions += ["Throw"]

        self.collected_rewards = []

        self.ball = Ball(np.array([0, 0, 0]), 0.15)
        self.target = Target(np.array([2.0, 10.0, 2.0]), 0.5)

        q = np.array([0, 0, 0, np.pi / 2, 0, 0, 0])
        self.robot = simple_human_arm(1.0, 1.0, q, np.array([2.0, 2.0, 2.0]))

        self.env = Environment(dimensions=np.array([10.0, 10.0, 20.0]),
                               dynamic_objects=[ball],
                               static_objects=[target],
                               robot=self.robot)
        
        

    def observe(self):
        pass

    def perform_action(self, action):
        pass

    def is_over(self):
        pass

    def collect_reward(self, action):
        # TODO: Add to collected_rewards
        pass


    

    
