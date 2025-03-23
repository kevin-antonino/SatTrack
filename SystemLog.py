import numpy as np
import matplotlib.pyplot as plt

class SystemLog:
    def __init__(self, in_sys):
        self.system = in_sys
        self.init_log()

    def init_log(self):
        self.state_trajectory      = self.system._DynamicSystem__state
        self.derivative_trajectory = self.system._DynamicSystem__derivative
        self.input_trajectory      = self.system._DynamicSystem__input
        self.output_trajectory     = self.system._DynamicSystem__output
        self.time = self.system._DynamicSystem__time_stamp

    def log_trajectory(self):
        self.state_trajectory = np.append(self.state_trajectory, self.system._DynamicSystem__state.reshape(-1, 1), axis = 1)
        self.derivative_trajectory = np.append(self.derivative_trajectory, self.system._DynamicSystem__derivative.reshape(-1, 1), axis = 1)
        if self.system._DynamicSystem__input is not None:
            self.input_trajectory = np.append(self.input_trajectory, self.system._DynamicSystem__input.reshape(-1, 1), axis = 1)
        self.output_trajectory = np.append(self.output_trajectory, self.system._DynamicSystem__output.reshape(-1, 1), axis = 1)
        self.time = np.append(self.time, self.system._DynamicSystem__time_stamp)

    def plot_state(self):
        n_states = self.state_trajectory.shape[0]

        fig, axes = plt.subplots(n_states, 1)
        for ii in range(0, n_states):
            axes[ii].plot(self.time, self.state_trajectory[ii])

        plt.show()
