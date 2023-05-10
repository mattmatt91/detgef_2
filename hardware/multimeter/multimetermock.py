import random
import time

address = 'USB0::0x2A8D::0x5101::MY58018230::INSTR'

class MultimeterMock():
    def __init__(self):
        self.aperture = 0.06
        self.nplc = 1
        self.aper = True
      

    def init_device(self):
        pass

    def get_errors(self):
        err = "no errors"
        return err

    def get_data(self):
        sensors = ['S1', 'S2', 'S3', 'S4']
        data = [i*random.uniform(0.1, 1.1)for i in [12341234,6545645,453542,65546456]]
        result = {}
        for sensor, value in zip(sensors, data):
            result[sensor] = value
        return result

    def close(self):
        ...


if __name__ == '__main__':
    keysightdaq970a = Multimeter(address)
    print(keysightdaq970a.get_errors())
    print(keysightdaq970a.get_data())
    print(keysightdaq970a.get_errors())
    if 1:
        for i in range(10):
            print(keysightdaq970a.get_data())
            print(keysightdaq970a.get_errors())
            time.sleep(1)
    keysightdaq970a.close()
