import pyvisa
from time import sleep


address = 'COM22'

class Powersupply():
    def __init__(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        self.client = rm.open_resource(address)
        self.reset()
        # self.get_info()

    def reset(self):
        self.client.write('*RST')
        self.client.write('SYST:LOCK ON')
        self.client.write('POW:STAG:AFT:REM AUTO')
        self.client.write('SYST:CONF:OUTP:REST AUTO')
        sleep(1)

    def get_info(self):
        string = self.client.query('*IDN?')
        return string

    def close(self):
        self.client.close()
    
    # SETTER FUNCTIONS

    def set_voltage(self, voltage):
        while self.get_voltage_set() != voltage:
            sleep(0.1)
            # print(f'setting voltage to {voltage}')
            self.client.write(f'VOLT {float(voltage)}')
            sleep(0.1)

    def set_current(self, current):
        while self.get_current_set() != current:
            sleep(0.1)
            self.client.write(f'CURR {float(current)}')
            sleep(0.1)


    def set_power(self, power):
        while self.get_power_set() != power:
            sleep(0.1)
            self.client.write(f'POW {float(power)}')
            sleep(0.1)

    # GETTER FUNCTIONS
    def get_output(self):
        string = self.client.query(f'OUTPut?')
        return string

    def get_voltage_set(self):
        string = self.client.query(f'VOLT?')
        return float(string.split()[0])

    def get_current_set(self):
        string = self.client.query(f'CURR?')
        return float(string.split()[0])

    def get_power_set(self):
        string = self.client.query(f'POWER?')
        return float(string.split()[0])

    def get_voltage_actual(self):
        string = self.client.query(f'MEAS:VOLT?')
        return float(string.split()[0])

    def get_current_actual(self):
        string = self.client.query(f'MEAS:CURR?')
        return float(string.split()[0])

    def get_power_actual(self):
        string = self.client.query(f'MEAS:POW?')
        return float(string.split()[0])

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
        while self.get_output().find('ON')<0:
            sleep(0.1)
            self.client.write('OUTP ON')
            sleep(0.1)

    def supply_off(self):
        while self.get_output().find('OFF')<0:
            sleep(0.1)
            self.client.write('OUTP OFF')
            sleep(0.1)

    def get_errors(self):
        string = self.client.query('SYSTEM:ERROR:ALL?')
        return string.split(',')

if __name__ == '__main__':
    powersupply = Powersupply()
    i = 0
    powersupply.supply_on()
    powersupply.set_voltage(2)
    powersupply.set_current(10)  # was ist der senke betrieb?
    powersupply.set_power(200)
    for i in range(10):

        powersupply.set_voltage(i%5)
        print(powersupply.get_data())
        sleep(1)


    powersupply.supply_off()
    powersupply.close()