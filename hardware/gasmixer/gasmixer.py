
import serial
import json

port = "COM1"
baudrate = 9600

class Gasmixer():
    def __init__(self) -> None:
        self.channels = read_json("hardware\\gasmixer\\config.json")
        self.args = {
                    "port":port,
                    "baudrate":9600,
                    "xonxoff":True,
                    "timeout":1,
                    "parity":serial.PARITY_ODD,
                    "stopbits":serial.STOPBITS_ONE,
                    "bytesize":serial.EIGHTBITS
                    }

    def get_id(self):
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii('ID R \r\n'))
            id = ser.readline().decode("utf-8")
            print(f'connected with: {ser.portstr}')
            print(f'gas controller: {id}')
            return id

    def reset(self):
        with serial.Serial(**self.args) as ser:
            ser.write(self.convert_to_ascii('RE\r\n'))
    
    
    def close_valve_cnl(self, cnl):  # , set flow for cnl
        _cnl = self.channels[cnl]['channel']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'OF{_cnl}\r\n'))
    
    def open_valve_cnl(self, cnl):  # set flow for cnl
        _cnl = self.channels[cnl]['channel']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'ON{_cnl}\r\n'))

    def get_flow_set(self, cnl):
        _cnl = self.channels[cnl]['cnl']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'FS{_cnl}R\r\n'))
            response = byteslist_to_float(ser.readlines())
            # does this function work well?
            value = (response/1000) * self.channels[cnl]['flow_max']
            return value

    def get_flow_act(self, cnl):  # returns the actual concentraion
        # check which format is returned !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        _cnl = self.channels[cnl]['cnl']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'FL{_cnl}\r\n'))
            response = byteslist_to_float(ser.readlines())
            # does this function work well?
            value = (response/1000) * self.channels[cnl]['flow_max']
            return value

    def get_gfc(self, cnl):
        _cnl = self.channels[cnl]['cnl']
        with serial.Serial(**self.args) as ser:
            ser.write(convert_to_ascii(f'GC{_cnl}R\r\n'))
            response = byteslist_to_float(ser.readlines())
            return response


    def get_flow_set_all_cnls(self):
        response = {}
        for cnl in self.channels:
            response[cnl] = self.get_flow_set(cnl)
        return response

    def get_flow_act_all_cnls(self):
        response = {}
        for cnl in self.channels:
            response[cnl] = self.get_flow_act(cnl)
        return response

    def get_gfc_all_cnls(self):
        response = {}
        for cnl in self.channels:
            response[cnl] = self.get_gfc(cnl)
        return response

    def close_all_valves(self):
        for cnl in self.channels:
            self.close_valve_cnl(cnl)
    
    def open_all_valves(self):
        for cnl in self.channels:
            self.open_valve_cnl(cnl)

    def set_gfc(self, cnl, factor):  # values between 10 and 180, set flow for cnl
        _cnl = self.channels[cnl]['cnl']
        self.ser.write(self.convert_to_ascii(f'GC{_cnl}{factor}\r'))
        if self.get_gfc(cnl) != factor:  # check if value has benn set
            print(f'Failed to set gasfactor correction for cnl {cnl}')

    def set_gfc_all_cnl(self):
        for cnl in self.channels:
            self.set_gfc(cnl, self.channels[cnl]['correction_factor'])

    def set_flow_cnl(self, cnl, flow):  # values between 0 and 1000, set flow for cnl
        _cnl = self.channels[cnl]['cnl']
        self.ser.write(self.convert_to_ascii(f'FS{_cnl} {flow}\r\n'))
        if self.get_flow_set(cnl) != flow:  # check if value has benn set
            print(f'Failed to set flow for cnl {cnl}')

    def set_flow_ppm(self, flow, ppm):  # set the global flow and ppn of analyt
        self.flow = flow
        self.ppmH2 = ppm
        proportionH2 = (self.ppmH2/self.channels['H2']['ppm'])
        proportionWet = 0.5
        proportionDry = 1 - proportionH2 - proportionWet
        proportions = {'air_dry': proportionDry,
                       'air_wet': proportionWet, 'H2': proportionH2}
        print(proportions)
        mapped_values = self.proportions_to_promil(proportions)
        print(mapped_values)
        for cnl in self.channels:
            self.set_flow_cnl(cnl, mapped_values[cnl])

    def proportions_to_promil(self, proportions):
        mapped_values = {}
        for cnl in proportions:
            abs_value = proportions[cnl]*self.flow
            if self.channels[cnl]['flow_min'] <= abs_value and self.channels[cnl]['flow_max'] >= abs_value:
                mapped_values[cnl] = int(
                    (abs_value/self.channels[cnl]['flow_max'])*1000)
            else:
                return Exception(f"flow ({abs_value}ml) out of range for cnl {cnl} ")
        return mapped_values

def convert_to_ascii(text):
        ascii = [ord(i) for i in text]
        return ascii

def read_json(path: str):
    f = open(path)
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
    gasmixer.open_all_valves()
    gasmixer.close_all_valves()