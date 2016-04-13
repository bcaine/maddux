
# coding: utf-8

# In[9]:

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

origin = np.array([0, 0, 0])
end = np.array([2, 10, 2])

v = end - origin
lamb = np.linspace(0, 1, 100)

x = origin[0] + lamb * v[0]
y = origin[1] + lamb * v[1]
z = origin[2] + lamb * 11.81 + -9.81 * lamb**2


# In[42]:

arm = np.array([2, 0, 0])
radius = 3.0

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

xa = (radius * np.outer(np.cos(u), np.sin(v)) +
     arm[0])
ya = (radius * np.outer(np.sin(u), np.sin(v)) +
     arm[1])
za = (radius * np.outer(np.ones(np.size(u)), np.cos(v)) +
     arm[2])


# In[43]:

fig = plt.figure(figsize=(8, 8))
ax = Axes3D(fig)
ax.plot_surface(xa, ya, za, rstride=4, cstride=4,
                color='b', linewidth=0, alpha=0.25)
ax.plot(x, y, z)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])
ax.set_ylim([0, 10])


plt.show()
