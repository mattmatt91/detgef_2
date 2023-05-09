
import serial
import json
from os.path import join
import time

port = "COM1"
baudrate = 9600

class Gasmixer():
    def __init__(self) -> None:
        self.channels = read_json("gasmixer\\config.json")
        self.args = {
                    "port":port,
                    "baudrate":9600,
                    "xonxoff":True,
                    "timeout":1,
                    "parity":serial.PARITY_ODD,
                    "stopbits":serial.STOPBITS_ONE,
                    "bytesize":serial.EIGHTBITS
                    }

    # system commands

    def get_id(self):
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii('ID R \r\n'))
            id = ser.readline().decode("utf-8")
            print(f'connected with: {ser.portstr}')
            print(f'gas controller: {id}')
            return id

    def reset(self):
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii('RE\r\n'))
    
    # init func
    def init_device(self):
        self.set_gfc('H2', self.channels['H2']['correction_factor'])
        self.set_gfc('air_wet', self.channels['air_wet']['correction_factor'])
        self.set_gfc('air_dry', self.channels['air_dry']['correction_factor'])

    # open and close mfscs
    def close_valve(self, cnl:str):  # , set flow for cnl
        channel = self.channels[cnl]['channel']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'OF{channel}\r\n'))
    
    def open_valve(self, cnl:str):  # set flow for cnl
        channel = self.channels[cnl]['channel']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'ON{channel}\r\n'))


    # get and set flow
    def set_gfc(self, cnl, factor):  # values between 10 and 180, set flow for cnl
        channel = self.channels[cnl]['channel']
        while self.get_gfc(cnl) != factor:
            with serial.Serial(**self.args) as ser:
                ser.write(convert_to_ascii(f'GC{channel}{factor}\r\n'))
                

    def set_flow(self, cnl:str, flow:int):  # values between 0 and 1000, set flow for cnl
        channel = self.channels[cnl]['channel']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'FS{channel} {flow}\r\n'))
                

    def get_flow_set(self, cnl):
        channel = self.channels[cnl]['channel']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'FS{channel}R\r\n'))
            response = byteslist_to_float(ser.readlines())
            # does this function work well?
            value = (response/1000) * self.channels[cnl]['flow_max']
            return value

    def get_flow_act(self, cnl): 
        channel = self.channels[cnl]['channel']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'FL{channel}\r\n'))
            response = byteslist_to_float(ser.readlines())
            # does this function work well?
            value = (response/1000) * self.channels[cnl]['flow_max']
            return value

    def get_gfc(self, cnl):
        channel = self.channels[cnl]['channel']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'GC{channel}R\r\n'))
            response = byteslist_to_float(ser.readlines())
            return response

    def get_data(self):

        data = {}
        with serial.Serial(**self.args) as ser:
            for channel in self.channels:
                channel_number = self.channels[channel]['channel']
                # flow set
                ser.write(convert_to_ascii(f'FS{channel_number}R\r\n'))
                response = byteslist_to_float(ser.readlines())
                value = (response/1000) * self.channels[channel]['flow_max']
                data[f'{channel}_set'] = value
                # flow actual
                channel_number = self.channels[channel]['channel']
                ser.write(convert_to_ascii(f'FL{channel_number}\r\n'))
                response = byteslist_to_float(ser.readlines())
                value = (response/1000) * self.channels[channel]['flow_max']
                data[f'{channel}_act'] = value
        return data

# some helpers 
def convert_to_ascii(text):
        ascii = [ord(i) for i in text]
        return ascii

def read_json(path: str):
    try:
        f = open(path)
        data = json.load(f)
        f.close()
    except:
        f = open(join('hardware',path))
        data = json.load(f)
        f.close()
    return data

def convert_to_ascii(text):
        ascii = [ord(i) for i in text]
        return ascii

def byteslist_to_float(list_of_bytes):
        value = float(''.join([i.decode() for i in list_of_bytes]))
        return value


if __name__ == '__main__':
    gasmixer = Gasmixer()
    gasmixer.get_id()
    gasmixer.init_device()
    gasmixer.set_flow('H2', 500)
    gasmixer.set_flow('air_dry', 500)
    gasmixer.set_flow('air_wet', 200)
    mytime = time.time()
    print(gasmixer.get_data())
    print(f'duration: {time.time()-mytime}')