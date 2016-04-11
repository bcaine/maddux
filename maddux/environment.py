"""
Our experiment environment.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

from objects import Ball, Target

class Environment:

    def __init__(self, ball, target, robot=None, dimensions=None):
        """
        Our room goes from [0, 0, 0] to [x, y, z]
        :param dimensions: 1x3 array of the dimensions of the room.
        """
        self.ball = ball
        self.target = target
        self.robot = robot
        if dimensions:
            self.dimensions = dimensions
        else:
            self.dimensions = np.array([10.0, 10.0, 100.0])


    def run(self, duration):
        """Run for a certain duration
        
        :param duration: duration to run environment in ms
        :return score: The value showing how close the ball is to the target
        """

        for _ in xrange(duration):
            self.ball.step()
            if self._collision():
                break
        return self.target.get_score(self.ball.leading_point())

    
    def _collision(self):
        """Check if the object collides with the walls
        :return: Boolean, whether there was a collision
        """
        if self.ball.attached:
            return False
        
        if self.target.is_hit(self.ball):
            self.ball.attach()
            return True

        for i in range(len(self.ball.position)):
            if (self.ball.position[i] <= 0
                or self.ball.position[i] >= self.dimensions[i]):
                self.ball.attach()
                return True

        return False
            
                    
    def plot(self, ax=None, show=True):
        """Plot throw trajectory and ball

        :param ax: Current axis if a figure already exists
        :param show: (Default: True) Whether to show the figure
        """
        if ax is None:
            fig = plt.figure(figsize=(12, 12))
            ax = Axes3D(fig)
        
        # Set the limits to be environment ranges
        ax.set_xlim([0, self.dimensions[0]])
        ax.set_ylim([0, self.dimensions[1]])
        ax.set_zlim([0, max(10, self.ball.positions[:, 2].max())])

        # Plot Trajectory
        ax.plot(self.ball.positions[:, 0], self.ball.positions[:, 1],
                self.ball.positions[:, 2], label='Trajectory')

        # Plot objects
        self.ball.plot(ax)
        self.target.plot(ax)

        if show:
            plt.show()


    def animate(self, duration):
        """Animates the running of the program
        
        :param duration: Duration of animation (at 30 fps)
        """

        def update(i):
            ax.clear()
            self.ball.step()
            self.plot(ax=ax, show=False)
            self._collision()

        fig = plt.figure(figsize=(8, 8))
        ax = Axes3D(fig)
        self.plot(ax=ax, show=False)
        
        ani = animation.FuncAnimation(fig, update, frames=duration,
                                      blit=False)
        plt.show()
