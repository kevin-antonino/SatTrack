from ForwardEuler import ForwardEuler
from SystemLog import SystemLog
import numpy as np

class DynamicSystem:
    def __init__(self, n_states, n_inputs, n_outputs):
        # State, derivative, input, and output variables. All column vectors
        self.__state = np.zeros((n_states,1))
        self.__derivative = np.zeros((n_states,1))
        self.__input = np.zeros((n_inputs,1))
        self.__output = np.zeros((n_outputs,1))
        self.__time_stamp = 0

        # Log trajectories and plotting 
        self.log = SystemLog(self)

        # Integrator
        self.__explicit_integrator = ForwardEuler() 

        # Inter-system communication attributes
        self.__input_map = ([], [])
        self.__input_systems = set()
        self.__output_systems = set()

    def initialize(self, x0, t0=0):
        self.__state = x0
        self.__time_stamp = t0
        self.check_inputs_and_update(t0)
        self.log.init_log()

    @staticmethod
    def dynamic_equation(x, u, t):
        return np.zeros((len(x),1))
    
    @staticmethod
    def output_equation(x, u, t):
        return np.zeros((len(x),1))
    
    def propagate_to(self, future_time):
        if self.__time_stamp < future_time:
            self.__state = self.__explicit_integrator.integrate_system_dynamics(self.__state, self.__input, self.dynamic_equation, self.__time_stamp, future_time);
            self.check_inputs_and_update(future_time)

        elif (self.__time_stamp > future_time):
            raise ValueError("Bad time")
    
    def check_inputs_and_update(self, future_time):
        if len(self.__input_systems) == 0 or all(self.__input_systems.__time_stamp == future_time):
            self.__input = self.pull_inputs()
            self.__derivative = self.dynamic_equation(self.__state, self.__input, self.__time_stamp)
            self.__output  = self.output_equation(self.__state, self.__input, self.__time_stamp)
            self.__time_stamp = future_time

            self.log.log_trajectory()
            self.notify_output_systems()

    def notify_output_systems(self):
        if len(self.__output_systems) > 0:
            for sys in self.__output_systems:
                sys.check_inputs_and_update(self.__time_stamp)

    def connect_input(self, input_sys, output_indeces):
        # add a break if connect_input is used twice on the same input_sys
        input_sys.__output_systems.add(self)
        self.__input_systems.add(input_sys)

        for out_idx in output_indeces:
            self.__input_map[0].append(input_sys)
            self.__input_map[1].append(out_idx)

    def pull_inputs(self):
        if len(self.__input_systems) == 0:
            return
        else:
            n_inputs = self.__input.shape[0]
            pulled_input = np.nan((n_inputs,1))
            for ii in range((0, n_inputs)):
                pulled_input[ii] = self.__input_map[0][ii].__output[self.__input_map[1][ii]]
