import numpy as np
from maddux.robots import simple_human_arm

np.set_printoptions(suppress=True)

# Create arm
q0 = np.array([0, -np.pi/4, 0, -np.pi/4, 0, 0, 0])
arm = simple_human_arm(2, 1, q0)

# Calculate jacobian on that joint config
print arm.jacob0(q0)
