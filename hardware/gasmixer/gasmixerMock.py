import json
from os.path import join
import time
import random



port = "COM1"
baudrate = 9600

class GasmixerMock():
    def __init__(self) -> None:
        self.channels = read_json("gasmixer\\config.json")
        self.gfc = {}
        self.flow_set = {}
        for i in self.channels:
            self.flow_set[i] = 0
            self.gfc[i] = 0

    # system commands

    def get_id(self):
        return "Mock Gasmixer"

    def reset(self):
        ...
    
    # init func
    def init_device(self):
        self.set_gfc('H2', self.channels['H2']['correction_factor'])
        self.set_gfc('air_wet', self.channels['air_wet']['correction_factor'])
        self.set_gfc('air_dry', self.channels['air_dry']['correction_factor'])


    # open and close mfscs
    def close_valve(self, cnl:str):  # , set flow for cnl
        ...
    
    def open_valve(self, cnl:str):  # set flow for cnl
        ...


    # get and set flow
    def set_gfc(self, cnl, factor):  # values between 10 and 180, set flow for cnl
        self.gfc[cnl] = factor
                

    def set_flow(self, cnl:str, flow:int):  # values between 0 and 1000, set flow for cnl
        flow = flow /1000
        flow = self.channels[cnl]['flow_max']*flow
        self.flow_set[cnl]= flow

    def get_flow_set(self, cnl):
        return self.flow_set[cnl]

    def get_flow_act(self, cnl): 
        return self.flow_set[cnl]*random.uniform(0.1, 1.1)

    def get_gfc(self, cnl):
      
        return self.gfc[cnl]

    def get_data(self):
        data = {}
        for channel in self.channels:
            value = self.get_flow_set(channel)
            data[f'{channel}_set'] = value        
            value = self.get_flow_set(channel)*random.uniform(0.1, 1.1)
            data[f'{channel}_act'] = value
        return data

# some helpers 


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