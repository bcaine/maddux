import numpy as np
from maddux.robots import simple_human_arm

def find_jacob0():
    """Show how to calculate the jacobian of am arm."""

    np.set_printoptions(suppress=True)
    
    # Create arm
    q0 = np.array([0, -np.pi / 4, 0, -np.pi / 4, 0, 0, 0])
    arm = simple_human_arm(2, 1, q0)
    
    # Calculate jacobian on that joint config
    print arm.jacob0(q0)

if __name__ == '__main__':
    find_jacob0()
