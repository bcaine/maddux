"""
Maddux is an experiment with Reinforcement Learning
on Robot Arms, teaching them to throw.

Written from scratch because we're masochists.

This may make more sense as a library than a CLI.
Rethink this when we get a bit further along
"""

import argparse
from tests import run_test, tests


def main():
    parser = argparse.ArgumentParser(
        description="Reinforcement Learning for robot arm throwing")
    parser.add_argument('-t', '--test', type=str, required=True,
                        help="Which test to run.")

    args = parser.parse_args()

    if not run_test(args.test):
        parser.print_help()
        print "Test Options: {}".format(tests.keys())

if __name__ == "__main__":
    main()
