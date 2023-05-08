from fastapi import FastAPI
from random import randint
from datetime import datetime
# from relais.relais import Relais
# from multimeter.multimetermock import MultimeterMock
# from powersupply.powersupply import Powersupply
# from gasmixer.gasmixer import Gasmixer

app = FastAPI()

# multimeter = MultimeterMock()
# powersupply = Powersupply()
# gasmixer = Gasmixer()
# relais = Relais()

@app.get("/get_data")
def get_sensor_data():
    # data_powersupply_set = powersupply.get_all_set()
    # data_powersupply_actual = powersupply.get_all_actual()

    # data_multimeter = multimeter.get_data()

    # data_gasmixer = gasmixer.get_data()

    # data = data_powersupply_actual | data_powersupply_set | data_multimeter | data_gasmixer
    print(data)
    data = {
            "timestamp": datetime.now().strftime("%m/%d/%Y - %H:%M:%S"),
            "voltage": randint(1, 5),
            "current": randint(3, 6),
            "res_1": randint(300, 600),
            "res_2": randint(300, 600),
            "res_3": randint(300, 600),
            "res_4": randint(300, 600),
            "flow_mfc1":  randint(300, 600)/100,
            "flow_mfc2": randint(300, 600)/100,
            "flow_mfc3": randint(300, 600)/100,
            "flow_mfc4": randint(300, 600)/100,
            "relais1": randint(0, 1),
            "relais2": randint(0, 1),
            "relais3": randint(0, 1),
            "relais4": randint(0, 1),
        }
    return data


@app.post("/set_data")
def set_relais(data: dict):
    print(data)
    response = True
    return {
        "success": response
    }
