import pyvisa
import time

address = 'USB0::0x2A8D::0x5101::MY58018230::INSTR'

class Multimeter():
    def __init__(self, address:str):
        rm = pyvisa.ResourceManager()
        print(rm.list_resources())
        self.client = rm.open_resource(address)
        self.aperture = 0.06
        self.nplc = 1
        self.aper = True
        self.client.timeout = 10000  # set a delay
        self.client.read_termination = '\n'
        self.scanlist = "(@101) # ,102,103,104)"
        print(self.client.query("*IDN?"))
        self.client.write("*RST")
        self.client.write(":SYSTem:BEEPer:STATe 0")

        # set resistance
        self.client.write(f"SENSe:RESistance {self.scanlist}")

        # set autorange
        self.client.write("CONF:RES")
        self.client.write("RES:RANG:AUTO 1")

        # aperture or nplc
        if self.aper:
            # disables aperture
            self.client.write(f"CONF:FRES")
            self.client.write(f"FRES:NPLC {self.nplc}")
        else:
            self.client.write(
                f":SENSe:RESistance:APERture:ENABle 1")
            self.client.write(
                f":SENSe:RESistance:APERture {self.aperture}")

    def init_device(self):
        pass

    def get_errors(self):
        err = self.client.query("SYST:ERR?")
        return err

    def get_data(self):
        sensors = ['S1', 'S2', 'S3', 'S4']
        data = self.client.query(f"READ?")
        data = [float(i) for i in data.split(',')]
        result = {}
        for sensor, value in zip(sensors, data):
            result[sensor] = value
        return result

    def close(self):
        self.client.close()


if __name__ == '__main__':
    keysightdaq970a = Multimeter(address)
    print(keysightdaq970a.get_errors())
    print(keysightdaq970a.get_data())
    print(keysightdaq970a.get_errors())
    if 0:
        for i in range(10):
            print(keysightdaq970a.get_data())
            print(keysightdaq970a.get_errors())
            time.sleep(1)
    keysightdaq970a.close()
