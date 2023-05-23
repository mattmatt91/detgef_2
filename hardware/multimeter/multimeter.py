
import pyvisa as visa
import sys

VISA_ADDRESS = 'USB0::0x2A8D::0x5101::MY58018230::0::INSTR'

class Multimeter():
    def __init__(self):
        try:
            self.resourceManager = visa.ResourceManager()
            self.session = self.resourceManager.open_resource(VISA_ADDRESS)
        except visa.Error as ex:
            print('Couldn\'t connect to \'%s\', exiting now...' % VISA_ADDRESS)
            sys.exit()
        self.session.read_termination = '\n'

        # self.session.write('*IDN?')
        # idn = self.session.read()
        # print('*IDN? returned: %s' % idn.rstrip('\n'))

    def init_device(self):
        # self.session.write("SET DefaultTimeout to 10")
        # self.session.write(":CONFigure:RESistance (@201,202,203,204)")
        # print(self.session.read())
        # self.session.write(f"RES:NPLC 1")
        self.session.write(":ROUTe:SCAN (@201,202,203,204)")
        self.session.write("RES:RANG:AUTO 1")

    def get_errors(self):
        err = self.session.query("SYST:ERR?")
        return err

    def get_data(self):
        sensors = ['S1', 'S2', 'S3', 'S4']
        self.session.write(f"INIT")
        self.session.write(':FETCh?')
        data = self.session.read()
        data = [float(i) for i in  data.split(',')]
        data_dict = {}
        for sensor, value in zip(sensors, data):
            data_dict[sensor] = value
        return data_dict


    def close(self):
        self.session.close()
        self.resourceManager.close()


if __name__ == '__main__':
    multimeter = Multimeter()
    multimeter.init_device()
    try:
        # pass
        for i in range(5):
            print(multimeter.get_data())
    except KeyboardInterrupt:
        pass
    finally:
            multimeter.close()