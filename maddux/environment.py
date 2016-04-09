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
            if self._is_collision(ball, target):
                break
        return target.get_score(ball.leading_point())

    
    def _is_collision(self, ball, target):
        """Check if the object collides with the walls
        
        :param ball: Our ball object
        :param target: Our target object
        
        :return: Boolean, whether there was a collision
        """
        if target.is_hit(ball):
            ball.attach()
            return True

        for i, obj_dim in obj.position:
            if obj_dim <= 0 or obj_dim >= self.dimensions[i]:
                obj.attach()
                return True

        return False
            
                    
