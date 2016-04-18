"""
Maddux is an experiment with Reinforcement Learning
on Robot Arms, teaching them to throw.

Written from scratch because we're masochists.

This may make more sense as a library than a CLI.
Rethink this when we get a bit further along
"""
import argparse
import warnings
import sys
from maddux.examples import run_example, examples
from maddux.utils import run_util, utils

class HelpfulParser(argparse.ArgumentParser):

    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        print "Examples: {}".format(examples.keys())
        print "Utils: {}".format(utils.keys())
        sys.exit(2)


def main():
    parser = HelpfulParser(description="A robotic arm toolbox")
    parser.add_argument('-e', '--example', type=str, required=False,
                        help="Which example to run.")
    parser.add_argument('-u', '--util', type=str, required=False,
                        help="Run a utility. May require additional args")
    parser.add_argument('-i', '--input', type=str, required=False,
                        help="A path to an input file")
    parser.add_argument('-o', '--output', type=str, required=False,
                        help="A path to an output file")

    success = False
    if len(sys.argv):
        args = parser.parse_args()
        if args.example:
            success = run_example(args.example)
        elif args.util:
            success = run_util(**vars(args))

    if not success:
        parser.print_help()
        print "Examples: {}".format(examples.keys())
        print "Utils: {}".format(utils.keys())


if __name__ == "__main__":
    main()
