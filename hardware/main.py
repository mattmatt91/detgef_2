from fastapi import FastAPI
from random import randint
from datetime import datetime
from relais.relais import Relais
from multimeter.multimetermock import MultimeterMock
from powersupply.powersupply import Powersupply
from gasmixer.gasmixer import Gasmixer

app = FastAPI()

multimeter = MultimeterMock()
powersupply = Powersupply()
gasmixer = Gasmixer()
relais = Relais()

@app.get("/get_data")
def get_sensor_data():
    data_powersupply = powersupply.get_data()
    data_multimeter = multimeter.get_data()
    data_gasmixer = gasmixer.get_data()
    data_relais = relais.get_all_states()

    data = {
            "timestamp": datetime.now().strftime("%m/%d/%Y - %H:%M:%S"),
            "voltage_set": data_powersupply['voltage_set'],
            "voltage_act": data_powersupply['voltage_actual'],
            "current_act": data_powersupply['current_actual'],
            "current_set": data_powersupply['current_set'],

            "res_1": data_multimeter['S1'],
            "res_2": data_multimeter['S2'],
            "res_3": data_multimeter['S3'],
            "res_4": data_multimeter['S4'],

            "flow_H2_set": data_gasmixer['H2_set'],
            "flow_air_dry_set": data_gasmixer['air_dry_set'],
            "flow_air_wet_set": data_gasmixer['air_wet_set'],

            "flow_H2_act": data_gasmixer['H2_act'],
            "flow_air_dry_act": data_gasmixer['air_dry_act'],
            "flow_air_wet_act": data_gasmixer['air_wet_act'],

            "relais1": data_relais['relais1'],
            "relais2": data_relais['relais2'],
            "relais3": data_relais['relais3'],
            "relais4": data_relais['relais4']
        }

    return data


@app.post("/set_data")
def set_relais(data: dict):
    powersupply.set_voltage(data['voltage'])
    
    relais.set_one(0, data['v1'])
    relais.set_one(1, data['v2'])
    relais.set_one(2, data['v3'])
    relais.set_one(3, data['v4'])

    gasmixer.set_flow('air_dry', data['air_dry'])
    gasmixer.set_flow('air_wet', data['air_wet'])
    gasmixer.set_flow('H2', data['H2'])

    multimeter.get_data()

    response = True
    return {
        "success": response
    }

@app.get("/start")
def set_start_param():
    gasmixer.init_device()

    powersupply.supply_on()
    powersupply.set_current(10)
    powersupply.set_power(200)

    relais.set_all_off()

    multimeter.init_device()

    print('setting up')
    return {'state':'started'}

@app.get("/stop")
def set_stop_param():
    powersupply.supply_off()
    powersupply.close()

    multimeter.close()

    print('setting end parameter')
    return {'state':'finished'}