
import serial
from time import sleep
port = "COM9"
baudrate = 9600

class Relais():
    def __init__(self) -> None:
        pass

    def set_all_on(self):
        with serial.Serial(port, baudrate, timeout=1) as ser:
            bytes_to_send = bytes([0xf0, 0x05, 0xff, 0x0d, 0x0a])
            ser.write(bytes_to_send)
            # response = ser.read(10)  # read up to 10 bytes
            # print(response)

    def set_all_off(self):
        with serial.Serial(port, baudrate, timeout=1) as ser:
            bytes_to_send = bytes([0xf0, 0x06, 0xff, 0x0d, 0x0a])
            ser.write(bytes_to_send)
            # response = ser.read(10)  # read up to 10 bytes
            # print(response)

    def set_one(self, number:int, state:bool):
        if state:
            cmd = 0x01
        else: 
            cmd = 0x00
        if number >15 or number < 0:
            raise ValueError("Input integer must be between 0 and 15")
        # number_b =  bytes([number])
        with serial.Serial(port, baudrate, timeout=1) as ser:
            bytes_to_send = bytes([0xf0, 0x03, number, cmd, 0xff, 0x0d, 0x0a])
            ser.write(bytes_to_send)
            # response = ser.read(10)  # read up to 10 bytes
            # print(response)

    def get_one_state(self, number:int):
        with serial.Serial(port, baudrate, timeout=1) as ser:
            bytes_to_send = bytes([0xf0, 0x01, number, 0xff, 0x0d, 0x0a])
            ser.write(bytes_to_send)
            buffer = b''
            while True:
                data = ser.read()
                buffer += data
                if data == b'\n':
                    break
            if buffer[0] == 0:
                return False
            elif buffer[0] == 0:
                return True
    
    def get_all_states(self):
        data = {}
        for i in range(15):
            data[f'relais{i}'] = self.get_one_state(i)
        return data


     


            


if __name__ == '__main__':
    relais = Relais()
    relais.set_all_off()
    while True:
        for i in range(16):
            relais.set_one(i, True)
        print(relais.get_all_states())
        sleep(0.1)
        for i in range(16):
            relais.set_one(i, False)
        print(relais.get_all_states())

        sleep(0.1)
        
        # relais.get_all_states()