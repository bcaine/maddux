import numpy as np
import sys
import argparse
from maddux.predefined_environments import environments


def main():
    """Run CLI to get animation arguments"""
    
    parser = argparse.ArgumentParser(description="Animate a given saved path")
    parser.add_argument('-i', '--input', type=str, required=True,
                        help="A path to an input file")
    parser.add_argument('-o', '--output', type=str, required=False,
                        help="A path to an output file")
    parser.add_argument('-e', '--environment', type=str, required=True,
                        help="An environment to simulate inside of")

    if len(sys.argv):
        args = parser.parse_args()

        input_path = args.input
        output_path = args.output
        env = args.environment
        animate_path(env, input_path, output_path)

    else:
        parser.print_help()


def animate_path(environment, input_file, output_file=None):
    """Load a saved path and animate it
    
    :param environment: The environment the path occured in
    :type environment: str
    
    :param input_file: The file holding the joint configs
    :type input_file: str
    
    :param output_file: The file to save the animation to as a .mp4
    :type output_file: str or None

    :rtpye: None
    """
    if environment in environments:
        env = environments[environment]()
    else:
        print "Please provide an environment from: {}".format(
            environments.keys())
        return

    # Load our saved path
    saved_path = np.load(input_file)
    env.robot.qs = saved_path

    if output_file is not None:
        env.animate(save_path=output_file)
    else:
        env.animate()


if __name__ == '__main__':
    main()
