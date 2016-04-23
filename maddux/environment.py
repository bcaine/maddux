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

        :param dimensions: (Optional) The dimensions of env
        :type dimensions: 1x3 numpy.array or None

        :param dynamic_objects: (Optional) A list of objects that can move
        :type dynamic_objects: list of maddux.objects.DynamicObject or None

        :param static_objects: (Optional) A list of stationary objects
        :type static_objects: list of maddux.objects.StaticObject or None

        :param robot: (Optional) A robot to simulate
        :type robot: maddux.robot.Arm or None

        :rtype: None
        """

        if dimensions is not None:
            self.dimensions = np.array(dimensions)
        else:
            self.dimensions = np.array([10.0, 10.0, 100.0])
        self.dynamic_objects = dynamic_objects if dynamic_objects else []
        self.static_objects = static_objects if static_objects else []
        self.robot = robot

    def run(self, duration):
        """Run for a certain duration

        :param duration: duration to run environment in seconds
        :type duration: integer

        :rtype: None
        """
        duration_ms = int(duration * 1000)

        for _ in xrange(duration_ms):
            map(lambda obj: obj.step(), self.dynamic_objects)
            if self.collision():
                break

    def animate(self, duration=None, save_path=None):
        """Animates the running of the program

        :param duration: (Optional) Duration of animation in seconds
        :type duration: int or None

        :param save_path: (Optional) Path to save mp4 in instead of displaying
        :type save_path: String or None

        :rtype: None
        """
        fps = 15
        dynamic_iter_per_frame = 10 * fps

        if duration is None:
            if self.robot is None:
                # Sensible Default
                frames = fps * 5
            else:
                frames = len(self.robot.qs)
        else:
            frames = int(fps * duration)

        def update(i):
            ax.clear()
            for _ in xrange(dynamic_iter_per_frame):
                map(lambda obj: obj.step(), self.dynamic_objects)
                # Check for collisions
                self.collision()
            if self.robot is not None:
                next_q = self.robot.qs[i]
                self.robot.update_angles(next_q)
            self.plot(ax=ax, show=False)

        fig = plt.figure(figsize=(8, 8))
        ax = Axes3D(fig)
        self.plot(ax=ax, show=False)

        # If we don't assign its return to something, it doesn't run.
        # Seems like really weird behavior..
        ani = animation.FuncAnimation(fig, update, frames=frames, blit=False)
        if save_path is None:
            plt.show()
        else:
            Writer = animation.writers['ffmpeg']
            writer = Writer(
                fps=fps, metadata=dict(
                    artist='Maddux'), bitrate=1800)
            ani.save(save_path, writer=writer)

    def hypothetical_landing_position(self):
        """Find the position that the ball would land (or hit a wall)

        :returns: Position (x, y, z) of hypothetical landing position of a
                  thrown object based on end effector velocity.
        :rtype: numpy.ndarray or None
        """
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
        """Check if any dynamic objects collide with any static
        objects or walls.

        :return: Whether there was a collision
        :rtype: bool
        """
        for dynamic in self.dynamic_objects:
            if dynamic.attached:
                continue

            for static in self.static_objects:
                if static.is_hit(dynamic.position):
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
        :type ax: matplotlib.axes

        :param show: (Default: True) Whether to show the figure
        :type show: bool

        :rtype: None
        """
        if ax is None:
            fig = plt.figure(figsize=(12, 12))
            ax = Axes3D(fig)

        # Set the limits to be environment ranges
        ax.set_xlim([0, self.dimensions[0]])
        ax.set_ylim([0, self.dimensions[1]])

        if self.dynamic_objects:
            zmax = max([o.positions[:, 2].max()
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
