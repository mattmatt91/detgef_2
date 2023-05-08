import pyvisa
from time import sleep


address = 'ASRL12::INSTR'

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
        print(string)

    
    # SETTER FUNCTIONS

    def set_voltage(self, voltage):
        try:
            while float(self.client.query('VOLTage?').split()[0]) != float(voltage):
                self.client.write(f'VOLT {float(voltage)}')
                sleep(0.5)
        except:
            print('cannot set value')

    def set_current(self, current):
        try:
            while float(self.client.query('CURRent?').split()[0]) != float(current):
                self.client.write(f'CURR {float(current)}')
                sleep(0.5)
        except:
            print('cannot set value')

    def set_power(self, power):
        try:
            while float(self.client.query('POWer?').split()[0]) != float(power):
                self.client.write(f'POW {float(power)}')
                sleep(0.5)
        except:
            print('cannot set value')

    # GETTER FUNCTIONS

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
                'current_set_ps': self.get_current_set(),
                'voltage_set_ps': self.get_voltage_set()}
        return data

    def get_all_actual(self):
        data = {'power_actual': self.get_power_actual(),
                'current_actual_ps': self.get_current_actual(),
                'voltage_actual_ps': self.get_voltage_actual()}
        return data

    def get_all_actual_arr(self):
        string = self.client.query(f'MEAS:ARR?')
        return string.split(',')

    # def get_data(self):
    #     try:
    #         data = self.get_all_actual() | self.get_all_set()
    #         return data
    #     except Exception as e:
    #         print(f'Error reading powersupply: {e}, returning empty dict')
    #         return {}

    def supply_on(self):
        self.client.write('OUTP ON')

    def supply_off(self):
        self.client.write('OUTP OFF')

    def get_errors(self):
        string = self.client.query('SYSTEM:ERROR:ALL?')
        return string.split(',')

    def close(self):
        self.supply_off()


if __name__ == '__main__':
    powersupply = Powersupply('ASRL12::INSTR')
    # powersupply = PowerSupply('ASRL5::INSTR')
    i = 0
    while True:
        i += 1
        i = i % 5
        powersupply.set_voltage(i)
        powersupply.supply_on()
        powersupply.set_current(10)  # was ist der senke betrieb?
        powersupply.set_power(200)
        sleep(1)
        powersupply.supply_off()
        sleep(1)
        print(powersupply.get_all_actual())
        print(powersupply.get_all_set())
        # print(powersupply.get_data())
        # print(powersupply.get_errors())
        # powersupply.get_data()