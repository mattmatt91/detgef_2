import requests
import time

ip = '192.168.1.22'
ip = '127.0.0.1'
port = '9010'


def test_set_data(data:dict):
        print(f'setting data: {data}')
        response = requests.post(f'http://{ip}:{port}/set_data', json=data)
        print(response.json())


def test_get_data():
    ...





if __name__ == '__main__':
    d = {'id': 'heatingup', 'voltage': 4, 'mfc1': 50, 'mfc2': 10, 'mfc3': 30, 'mfc4': 50, 'duration': 4}
    data = {'voltage':4, 'mfc1': 50, 'mfc2': 10, 'mfc3': 30}
    test_set_data(data)
    time.sleep(2)
    data = {'voltage':1, 'mfc1': 40, 'mfc2': 60, 'mfc3': 10}
    test_set_data(data)
    time.sleep(2)
    data = {'voltage':2, 'mfc1': 10, 'mfc2': 60, 'mfc3': 60}
    test_set_data(data)
