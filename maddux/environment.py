"""
Our experiment environment.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
            
                    
    def plot(self):
        """Plot throw trajectory and ball"""
        positions = np.array(self.ball.positions)

        # Plot the trajectory
        fig = plt.figure(figsize=(12, 12))
        ax = fig.gca(projection='3d')
        ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], label='Trajectory')

        # Plot the ball
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)

        xb = 2 * self.ball.radius * np.outer(np.cos(u), np.sin(v)) + self.ball.position[0]
        yb = 2 * self.ball.radius * np.outer(np.sin(u), np.sin(v)) + self.ball.position[1]
        zb = 2 * self.ball.radius * np.outer(np.ones(np.size(u)), np.cos(v)) + self.ball.position[2]
        ax.plot_surface(xb, yb, zb, rstride=4, cstride=4, color='g')

        # Plot the target
        xt = 2 * self.target.radius * np.outer(np.cos(u), np.sin(v)) + self.target.position[0]
        yt = self.target.position[1]
        zt = 2 * self.target.radius * np.outer(np.ones(np.size(u)), np.cos(v)) + self.target.position[2]
        ax.plot_surface(xt, yt, zt, color='b', linewidth=0, alpha=0.25)
        
        # Set the limits to be environment ranges
        ax.set_xlim([0, self.dimensions[0]])
        ax.set_ylim([0, self.dimensions[1]])
        ax.set_zlim([0, max(10, positions[:, 2].max())])
        plt.show()
        
