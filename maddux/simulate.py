"""
Simulate wraps the training and evaluation
of a given robot and environment.
"""

class Simulate(object):

    def __init__(self, path, environment, objects, robot):
        """
        :param path: A path to the weights (or where to save them)
        :param environment: An environment object containing dimensions
        :param objects: A list of objects to place in the environment
        :param robot: Our Robot Arm
        """
        self.path = path
        self.environment = environment
        self.objects = objects
        self.robot = robot


    def train(self, n_iters, learner, verbose=False):
        """Train the robot using a specified learning method.
        
        :param n_iters: Number of iterations
        :param learner: Learning algorithm.
        :param verbose: Verbosity of output (Default: False)
        """
        pass


    def evaluate(self, verbose=False):
        """Evaluate it at its given state
        
        :param verbose: Verbosity of output (Default: False)
        """
        pass
