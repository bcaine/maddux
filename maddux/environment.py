"""
Our experiment environment.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation


GRAVITY = -9.81


class Environment:

    def __init__(self, dimensions=None, dynamic_objects=None,
                 static_objects=None, robot=None):
        """An environment to run experiments in
        :param dimensions: (Optional) 1x3 array of the dimensions of env
        :param dynamic_objects: (Optional) A list of objects that can move
        :param static_objects: (Optional) A list of stationary objects
        :param robot: (Optional) A robot to simulate
        """
        if dimensions is None:
            self.dimensions = np.array(dimensions)
        else:
            self.dimensions = np.array([10.0, 10.0, 100.0])
        self.dynamic_objects = dynamic_objects if dynamic_objects else []
        self.static_objects = static_objects if static_objects else []
        self.robot = robot

    def run(self, duration):
        """Run for a certain duration
        :param duration: duration to run environment in seconds
        :return score: The value showing how close the ball is to the target
        """
        duration_ms = int(duration * 1000)

        for _ in xrange(duration_ms):
            map(lambda obj: obj.step(), self.dynamic_objects)
            if self.collision():
                break
        return self.target.get_score(self.ball.leading_point())

    def animate(self, duration):
        """Animates the running of the program
        :param duration: Duration of animation in seconds
        """
        # We want it at 30 fps
        frames = int(30 * duration)
        dynamic_iter_per_frame = int(1000 / 30)

        if self.robot:
            robot_iter_per_frame = max(1, int(len(self.robot.qs) / frames))

        def update(i):
            ax.clear()
            for _ in xrange(dynamic_iter_per_frame):
                map(lambda obj: obj.step(), self.dynamic_objects)
                # Check for collisions
                self.collision()
            if self.robot is not None:
                next_q = self.robot.qs[:i * robot_iter_per_frame + 1][-1]
                self.robot.update_angles(next_q)
            self.plot(ax=ax, show=False)

        fig = plt.figure(figsize=(8, 8))
        ax = Axes3D(fig)
        self.plot(ax=ax, show=False)

        # If we don't assign its return to something, it doesn't run.
        # Seems like really weird behavior..
        _ = animation.FuncAnimation(fig, update, frames=frames, blit=False)
        plt.show()

    def hypothetical_landing_position(self):
        """Find the position that the ball would land (or hit a wall)"""
        pos = self.robot.end_effector_position().copy()
        # Only need linear velocity
        v = self.robot.end_effector_velocity()[0:3]

        for t in np.linspace(0, 15, 5000):
            # Check if it hit a target
            for static in self.static_objects:
                if static.is_hit(pos):
                    return pos.copy()

            # Or a wall
            for i in range(len(pos)):
                in_negative_space = pos[i] <= 0
                past_boundary = pos[i] >= self.dimensions[i]

                if in_negative_space or past_boundary:
                    return pos.copy()

            # Otherwise step forward
            v[2] += t * GRAVITY
            pos += t * v
        # If we never hit anything (which is completely impossible (TM))
        # return None
        return None

    def collision(self):
        """Check if any dynamic objects collide with any static objects
        or walls.
        :return: Boolean, whether there was a collision
        """
        for dynamic in self.dynamic_objects:
            if dynamic.attached:
                continue

            for static in self.static_objects:
                if static.is_hit(dynamic.leading_point()):
                    dynamic.attach()
                    return True

            for i in range(len(dynamic.position)):
                in_negative_space = dynamic.position[i] <= 0
                past_boundary = (dynamic.position[i] >=
                                 self.dimensions[i])
                if in_negative_space or past_boundary:
                    dynamic.attach()
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

        if self.dynamic_objects:
          zmax = max([o.positions[:, 2].max() \
                      for o in self.dynamic_objects])
        else:
          zmax = 10
        ax.set_zlim([0, max(10, zmax)])

        # And set our labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        for dynamic in self.dynamic_objects:
            # Plot Trajectory
            ax.plot(dynamic.positions[:, 0], dynamic.positions[:, 1],
                    dynamic.positions[:, 2], 'r--', label='Trajectory')

        # Plot objects
        map(lambda obj: obj.plot(ax), self.dynamic_objects)
        map(lambda obj: obj.plot(ax), self.static_objects)

        if self.robot:
            self.robot.plot(ax)

        if show:
            plt.show()

    def plot_vpython(self):
        map(lambda obj: obj.plot(), self.dynamic_objects)
        map(lambda obj: obj.plot(), self.static_objects)

        if self.robot:
            self.robot.plot()

    def animate_vpython(self):
        pass
        

            
