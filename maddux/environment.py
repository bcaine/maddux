"""
Our experiment environment.
"""
import numpy as np
from objects import Ball, Target

class Environment:

    def __init__(self, dimensions=None):
        """
        Our room goes from [0, 0, 0] to [x, y, z]
        :param dimensions: 1x3 array of the dimensions of the room.
        """
        self.dimensions = dimensions if dimensions else np.array([10.0, 10.0, 100.0])
        self.objects = {}
        

    def add_object(self, obj):
        """
        :param obj: An object (like a ball, robot, or target) to add
                    to the environment.
        """
        self.objects[obj.name] = obj


    def run(self, duration):
        """Run for a certain duration
        
        :param duration: duration to run environment in ms

        :return score: The value showing how close the ball is to the target
        """
        assert "ball" in self.objects
        assert "target" in self.objects

        ball = self.objects["ball"]
        target = self.objects["target"]

        for _ in xrange(duration):
            ball.step()
            if self._is_collision(ball, target):
                break
        return target.get_score(ball.leading_point())

    
    def _is_collision(self, ball, target):
        """Check if the object collides with the walls
        
        :param ball: Our ball object
        :param target: Our target object
        """
        if target.is_hit(ball):
            ball.attach()
            return True

        for i, obj_dim in obj.position:
            # If in a negative dimension, or it hit a wall
            if obj_dim <= 0 or obj_dim >= self.dimensions[i]:
                # Attach it to that surface
                obj.attach()
                return True

        return False
            
                    
