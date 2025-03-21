class DynamicSystem:
    def __init__(self, n_states, n_inputs, n_outputs):
        # State, derivative, input, and output variables
        self.__state = np.zeros((n_states,1))
        self.__derivative = np.zeros((n_states,1))
        self.__input = np.zeros((n_inputs,1))
        self.__output = np.zeros((n_outputs,1))

        self.__integrator = RungeKutta()

        self.time_stamp = 0

        # Inter-system communication attributes
        self.__input_bus = SystemBus()
        self.__updated_systems = {};
        self.__input_systems = {};
        self.__output_systems = {};
    
    def dynamic_equation(x, u, t):
        return np.zeros((len(x),1))

    def output_equation(x, u, t):
        return np.zeros((len(x),1))
    
    def propagate_to(self, future_time):
        if (self.time_stamp < future_time):
            next_state = self.__integrator.integrate_system_dynamics(self.__state[:,-1], self.__input[:,-1], self.__dynamic_equation, self.time_stamp, future_time);
            self.__state = np.append(self.__state, next_state, axis=1)
            self.notify_output_systems()

        elif (self.time_stamp > future_time):
            raise ValueError("Bad time")
    
    def notify_output_systems(self):
        if (self.__output_systems.len() > 0):
            for sys in self.__output_systems:
                sys.await_and_update(self)

    def await_and_update(self, in_sys):
        self.__updated_systems.add(in_sys)

        if (sorted(self.__input_systems) == sorted(self.__updated_systems)):
            self.__input = np.append(self.__input, self.__input_bus.values, axis=1)
            
            next_derivative = self.dynamic_equation(self.__state[:,-1], self.__input[:,-1], self.time_stamp)
            self.__derivative = np.append(self.__derivative, next_derivative, axis=1)
            
            next_output = self.output_equation(self.__state[:,-1], self.__input[:,-1], self.time_stamp)
            self.__output = np.append(self.__output, next_output, axis=1)
            
    def connect_input(self, in_sys):
        in_sys.__output_systems.add(self)

