import requests
import time

ip = '192.168.1.22'
ip = '127.0.0.1'
port = '9010'


def test_sensors():
    ...
    # test get sensordata
    # response = requests.get(f'http://{ip}:{port}/watersystem_get_data_sensor')
    # print(response.json())

    # test get state pumps
    # response = requests.get(f'http://{ip}:{port}/watersystem_get_data_pumps')
    # print(response.json())

    # test set state
    # data = {"pump": "ph_up", "state": True}
    # requests.post(f'http://{ip}:{port}/watersystem_cmd', json=data)
    # response = requests.get(f'http://{ip}:{port}/watersystem_get_data_pumps')
    # print(response.json())
    # time.sleep(2)
    # data = {"pump": "ph_up", "state": False}
    # requests.post(f'http://{ip}:{port}/watersystem_cmd', json=data)





if __name__ == '__main__':

    test_sensors()
