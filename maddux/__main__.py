"""
Maddux is an experiment with Reinforcement Learning
on Robot Arms, teaching them to throw.

Written from scratch because we're masochists.

This may make more sense as a library than a CLI.
Rethink this when we get a bit further along
"""

import argparse
from simulate import Simulate


def main():
    parser = argparse.ArgumentParser(
        description="Reinforcement Learning for robot arm throwing")
    parser.add_argument('-t', '--train', action='store_true',
                        help='Train the robot')
    parser.add_argument('-e', '--evaluate', action='store_true',
                        help='Evaluate the arm by throwing once.')
    parser.add_argument('-p', '--path', type=str, required=True,
                        help='Path to weight file')

    args = parser.parse_args()

    if args.train:
        train(args.path)
    elif args.evaluate:
        evaluate(args.path)
    else:
        parser.print_help()


def train(path):
    """
    Train the robot arm with RL to throw a ball

    :param path: Path to save location of training data
    """
    pass


def evaluate(path):
    """
    Evaluate the robot arm throwing with RL

    :param path: Path to save location of the training data
    """
    pass


if __name__ == "__main__":
    main()
