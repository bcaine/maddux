"""
Our experiment environment.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation


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
            self.dimensions = np.array(dimensions)
        else:
            self.dimensions = np.array([10.0, 10.0, 100.0])

    def run(self, duration):
        """Run for a certain duration

        :param duration: duration to run environment in seconds
        :return score: The value showing how close the ball is to the target
        """
        duration_ms = int(duration * 1000)

        for _ in xrange(duration_ms):
            self.ball.step()
            if self._collision():
                self.ball.attach()
                break
        return self.target.get_score(self.ball.leading_point())

    def _collision(self):
        """Check if the object collides with the walls
        :return: Boolean, whether there was a collision
        """
        if self.ball.attached:
            return False

        if self.target.is_hit(self.ball.leading_point()):
            return True

        for i in range(len(self.ball.position)):
            in_negative_space = self.ball.position[i] <= 0
            past_boundary = self.ball.position[i] >= self.dimensions[i]
            if in_negative_space or past_boundary:
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

        # And set our labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        # Plot Trajectory
        ax.plot(self.ball.positions[:, 0], self.ball.positions[:, 1],
                self.ball.positions[:, 2], 'r--', label='Trajectory')

        # Plot objects
        self.ball.plot(ax)
        self.target.plot(ax)

        if self.robot:
            self.robot.plot(ax)

        if show:
            plt.show()

    def animate(self, duration):
        """Animates the running of the program

        :param duration: Duration of animation in seconds
        """
        # We want it at 30 fps
        frames = int(30 * duration)
        iter_per_frame = int(1000 / 30)

        def update(i):
            ax.clear()
            for _ in xrange(iter_per_frame):
                self.ball.step()
                if self._collision():
                    self.ball.attach()
            self.plot(ax=ax, show=False)

        fig = plt.figure(figsize=(8, 8))
        ax = Axes3D(fig)
        self.plot(ax=ax, show=False)

        # If we don't assign its return to something, it doesn't run.
        # Seems like really weird behavior..
        _ = animation.FuncAnimation(fig, update, frames=frames, blit=False)
        plt.show()
