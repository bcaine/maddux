"""
A base throwable object class that encodes traits like gravity,
velocity, etc.
"""
import numpy as np

GRAVITY=-9.81
TIME = 0.001

class ThrowableObject:

    def __init__(self, position):
        """Throwable Object Init"""
        self.position = position
        self.attached = True
        self.velocity = np.array([0, 0, 0])


    def throw(self, velocity):
        """Throw an object.
        
        :param velocity: 1x3 numpy array of object velocities
        """
        self.attached = False
        self.velocity = velocity

    
    def step(self):
        """Update one timestep (one ms)"""
        if not self.attached:
            self.velocity[2] += TIME * GRAVITY
            self.position += TIME * self.velocity

    
    def attach(self):
        self.attached = True
        

    def __str__(self):
        return """
        Position: {}
        Velocity: {}
        Attached: {}
        """.format(self.position, self.velocity, self.attached)
        
