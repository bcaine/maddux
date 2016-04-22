import numpy as np
from maddux.predefined_environments import predefined_environments

def animate_path(environment, input_file, output_file=None):
    """
    Load a saved path and animate it
    :param environment: The environment the path occured in
    :type environment: String
    :param input_file: The file holding the joint configs
    :type input_file: String
    :param output_file: The file to save the animation to as a .mp4
    :type output_file: String or None
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
