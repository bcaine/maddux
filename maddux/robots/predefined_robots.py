from link import Link
from arm import Arm
import numpy as np


def simple_human_arm(seg1_len, seg2_len, q0, base=None):
    """
    Creates a simple human-like robotic arm with 7 links and 2 segments
    with the desired lengths and starting joint configuration
    :param seg1_len: The length of the first segment of the arm
    :type seg1_len: integer
    :param seg2_len: The length of the second segment of the arm
    :type seg2_len: integer
    :param q0: The starting joint configuration
    :type q0: 1xN numpy.array
    :param base: (Optional) optional base location of arm
    :type base: 1x3 numpy.array or None
    :rtype: maddux.robot.Arm
    """
    L1 = Link(0, 0, 0, 1.571)
    L2 = Link(0, 0, 0, -1.571)
    L3 = Link(0, seg1_len, 0, -1.571)
    L4 = Link(0, 0, seg2_len, -1.571)
    L5 = Link(0, 0, 0, 1.571)
    L6 = Link(0, 0, 0, 1.571)
    L7 = Link(0, 0, 0, 0)
    links = np.array([L1, L2, L3, L4, L5, L6, L7])

    robot = Arm(links, q0, 'simple_human_arm', 4, base)
    return robot

def noodle_arm(seg_lens, q0, base=None):
    """
    Creates a complex arm with 10 segments
    :param seg_lens: The lengths of each sement
    :type seg_lens: 1x10 nump.array
    :param q0: The starting joint configuration
    :type 10: 1xN numpy.array
    :param base: (Optional) optional base location of arm
    :type base: 1x3 nump.array or None
    :rtype: maddux.robot.Arm
    """
    L1  = Link(0, seg_lens[0], 0, 1.571)
    L2  = Link(0, seg_lens[1], 0, -1.571)
    L3  = Link(0, seg_lens[2], 0, -1.571)
    L4  = Link(0, seg_lens[3], 0, 1.571)
    L5  = Link(0, seg_lens[4], 0, 1.571)
    L6  = Link(0, seg_lens[5], 0, -1.571)
    L7  = Link(0, seg_lens[6], 0, 1.571)
    L8  = Link(0, seg_lens[7], 0, 1.571)
    L9  = Link(0, seg_lens[8], 0, -1.571)
    L10 = Link(0, seg_lens[9], 0, 1.571)
    links = np.array([L1, L2, L3, L4, L5, L6, L7, L8, L9, L10])

    robot = Arm(links, q0, 'noodle_arm', 10, base)
    return robot
