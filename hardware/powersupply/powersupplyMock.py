from time import sleep
import random

address = 'ASRL12::INSTR'

class PowersupplyMock():
    def __init__(self):
        self.voltage_set = 0
        self.current_set = 0
        self.power_set = 0

    def reset(self):
        ...

    def get_info(self):
        return "Mock Powersupply"

    def close(self):
        ...
    
    # SETTER FUNCTIONS

    def set_voltage(self, voltage):
        self.voltage_set = voltage

    def set_current(self, current):
        self.current_set = current


    def set_power(self, power):
        self.power_set = power

    # GETTER FUNCTIONS

    def get_voltage_set(self):
        return self.voltage_set

    def get_current_set(self):
        return self.current_set

    def get_power_set(self):
        return self.power_set

    def get_voltage_actual(self):
        return self.voltage_set*random.uniform(0.1, 1.1)

    def get_current_actual(self):
        return 3*random.uniform(0.1, 1.1)

    def get_power_actual(self):
        6*random.uniform(0.1, 1.1)

    def get_all_set(self):
        data = {'power_set': self.get_power_set(),
                'current_set': self.get_current_set(),
                'voltage_set': self.get_voltage_set()}
        return data

    def get_all_actual(self):
        data = {'power_actual': self.get_power_actual(),
                'current_actual': self.get_current_actual(),
                'voltage_actual': self.get_voltage_actual()}
        return data

    def get_all_actual_arr(self):
        string = self.client.query(f'MEAS:ARR?')
        return string.split(',')

    def get_data(self):
        data = {'power_actual': self.get_power_actual(),
                'current_actual': self.get_current_actual(),
                'voltage_actual': self.get_voltage_actual(),
                'power_set': self.get_power_set(),
                'current_set': self.get_current_set(),
                'voltage_set': self.get_voltage_set()}
        return data

    def supply_on(self):
        ...

    def supply_off(self):
        ...

    def get_errors(self):
        return ""

if __name__ == '__main__':
    powersupply = Powersupply()
    i = 0
    powersupply.supply_on()
    powersupply.set_current(10)  # was ist der senke betrieb?
    powersupply.set_power(200)
    powersupply.set_voltage(2.4)
    # sleep(5)
    for i in range(10):

        powersupply.set_voltage(i%5)
        sleep(1)
        print(powersupply.get_data())


    powersupply.supply_off()
    powersupply.close()