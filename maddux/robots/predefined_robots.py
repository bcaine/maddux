from link import Link
from arm import Arm
import numpy as np


def simple_human_arm(seg1_len, seg2_len, q0, base=None):
    """
    Creates a simple human-like robotic arm with 5 links and 2 segments
    with the desired lengths and starting joint configuration
    :param seg1_len: The length of the first segment of the arm
    :param seg2_len: The length of the second segment of the arm
    :param q0: The starting joint configuration
    :param base: (Optional) optional base location of arm
    """
    L1 = Link(0, 0, 0, 1.571)
    L2 = Link(0, 0, 0, -1.571)
    L3 = Link(0, seg1_len, 0, -1.571)
    L4 = Link(0, 0, 0, 1.571)
    L5 = Link(0, seg2_len, 0, 1.571)
    links = np.array([L1, L2, L3, L4, L5])

    robot = Arm(links, q0, 'simple_human_arm', base)
    return robot
