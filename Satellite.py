import numpy as np

class Satellite:
    def __init__(self):
        # State
        self.q_BI   = np.array([0, 0, 0, 1]).T
        self.w_BI_B = np.array([0, 0, 0]).T

        # Sensors and Actuators
        self.reacton_wheel = IdealReactionWheel() 
        self.magnetorquer  = IdealMagnetorquer()

        # Control
        self.flight_computer 

        # Mass properties
        self.mass_prop
