
from time import sleep

class RelaisMock():
    def __init__(self) -> None:
        pass
        self.states = [False for i in range(16)]

    def set_all_on(self):
        self.states = [True for i in range(16)]

    def set_all_off(self):
        self.states = [False for i in range(16)]

    def set_one(self, number:int, state:bool):
        if number >15 or number < 0:
            raise ValueError("Input integer must be between 0 and 15")
        # number_b =  bytes([number])
        self.states[number] = state

    def get_one_state(self, number:int):
        return self.states[number]
    
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