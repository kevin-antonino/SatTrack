class ForwardEuler:
    def __init__(self):
        pass

    def integrate_system_dynamics(x0, u0, dx_dt, t0, tf):
        xf = (tf - t0) * dx_dt(x0, u0, t0) + x0
        return xf
    