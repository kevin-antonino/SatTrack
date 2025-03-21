class MassProperties:
    def __init__(self):
        # Dry Mass [kg]
        self.mass = 0
        
        # Moment of Inertia [kg * m^2] taken about center of mass in body coordinates
        self.__Ixx = 0 
        self.__Ixy = 0
        self.__Ixz = 0
        self.__Iyy = 0
        self.__Iyz = 0
        self.__Izz = 0

        self.MoI_cm_B = np.array([[self.Ixx, -self.Ixy, -self.Ixz],
                                  [-self.Ixy, self.Iyy, -self.Iyz],
                                  [-self.Ixz, -self.Iyz, self.Izz]])

