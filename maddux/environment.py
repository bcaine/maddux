"""
Our experiment environment.
"""
import numpy as np
from objects import Ball, Target

class Environment:

    def __init__(self, ball, target, robot=None, dimensions=None):
        """
        Our room goes from [0, 0, 0] to [x, y, z]
        :param dimensions: 1x3 array of the dimensions of the room.
        """
        self.dimensions = dimensions if dimensions else np.array([10.0, 10.0, 100.0])
        self.ball = ball
        self.target = target
        self.robot = robot


    def run(self, duration):
        """Run for a certain duration
        
        :param duration: duration to run environment in ms
        :return score: The value showing how close the ball is to the target
        """

        for _ in xrange(duration):
            self.ball.step()
            if self._is_collision():
                break
        return self.target.get_score(self.ball.leading_point())

    
    def _is_collision(self):
        """Check if the object collides with the walls
        :return: Boolean, whether there was a collision
        """
        if self.ball.attached:
            return False
        
        if self.target.is_hit(self.ball):
            self.ball.attach()
            return True

        for i in range(len(self.ball.position)):
            if self.ball.position[i] <= 0 or self.ball.position[i] >= self.dimensions[i]:
                self.ball.attach()
                return True

        return False
            
                    
