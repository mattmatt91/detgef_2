
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
            time.sleep(0.1)
            return id

    def reset(self):
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii('RE\r\n'))
            time.sleep(0.1)
    
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
            time.sleep(0.1)
    
    def open_valve(self, cnl:str):  # set flow for cnl
        channel = self.channels[cnl]['channel']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'ON{channel}\r\n'))
            time.sleep(0.1)
 
 
    def open_valve_0(self):  # set flow for cnl
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'ON 0\r\n'))
            time.sleep(0.1)

    def close_valve_0(self):  # set flow for cnl
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'OF 0\r\n'))
            time.sleep(0.1)


    # get and set flow
    def set_gfc(self, cnl, factor):  # values between 10 and 180, set flow for cnl
        channel = self.channels[cnl]['channel']
        while self.get_gfc(cnl) != factor:
            with serial.Serial(**self.args) as ser:
                ser.write(convert_to_ascii(f'GC{channel}{factor}\r\n'))
                time.sleep(0.1)
                

    def set_flow(self, cnl:str, flow:int):  # values between 0 and 1000, set flow for cnl
        channel = self.channels[cnl]['channel']
        max_flow = self.channels[cnl]['flow_max']
        new_flow = round((flow/max_flow)*1000)
        # print(new_flow, '\n'*100)
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'FS{channel} {new_flow}\r\n'))
            time.sleep(0.1)
                

  
    def get_setpiont(self, cnl): 
        channel = self.channels[cnl]['channel']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'FS{channel}R\r\n'))
            response = byteslist_to_float(ser.readlines())
            time.sleep(0.1)
            return response

    def get_flow_set(self, cnl):
        channel = self.channels[cnl]['channel']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'FS{channel}R\r\n'))
            response = byteslist_to_float(ser.readlines())
            # does this function work well?
            value = (response/1000) * self.channels[cnl]['flow_max']
            time.sleep(0.1)
            return value


    def get_flow_act(self, cnl): 
        channel = self.channels[cnl]['channel']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'FL{channel}\r\n'))
            response = byteslist_to_float(ser.readlines())
            value = (response/1000) * self.channels[cnl]['flow_max']
            time.sleep(0.1)
            return value

    def get_gfc(self, cnl):
        channel = self.channels[cnl]['channel']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'GC{channel}R\r\n'))
            response = byteslist_to_float(ser.readlines())
            time.sleep(0.1)
            return response

    def set_range(self, cnl):
        channel = self.channels[cnl]['channel']
        rng = self.channels[cnl]['flow_max']
        if rng == 500:
            rng_index = 8
        elif rng == 20:
            rng_index = 4
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'RA{channel} {rng_index}\r\n'))
            time.sleep(0.1)

    def get_data(self):
        data = {}
        with serial.Serial(**self.args) as ser:
            for channel in self.channels:
                channel_number = self.channels[channel]['channel']
                # flow set
                ser.write(convert_to_ascii(f'FS{channel_number}R\r\n'))
                time.sleep(0.1)
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
    gasmixer.init_device()

    gasmixer.set_range('H2')
    gasmixer.set_range('air_dry')
    gasmixer.set_range('air_wet')
    
    gasmixer.get_id()
    gasmixer.open_valve_0()
    gasmixer.open_valve('H2')
    gasmixer.open_valve('air_wet')
    gasmixer.open_valve('air_dry')
    gasmixer.set_flow('H2', 0)
    # print(gasmixer.get_setpiont('H2'))
    gasmixer.set_flow('air_dry', 400)
    gasmixer.set_flow('air_wet', 400)

    time.sleep(5)
    gasmixer.close_valve_0()
    # print(gasmixer.get_data())