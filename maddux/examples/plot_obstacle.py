from maddux.environment import Environment
from maddux.objects import Obstacle


def plot_obstacle():
    """Create and plot an obstacle within an environment."""
    obstacle = Obstacle([1.0, 1.0, 0.0], [2.0, 3.0, 5.0])
    env = Environment(dimensions=[10.0, 10.0, 10.0],
                      static_objects=[obstacle])
    env.plot()

if __name__ == '__main__':
    plot_obstacle()
