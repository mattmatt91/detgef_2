import sched
from helpers import helpers as hp
import time
import requests
from datetime import datetime, timedelta
from database.database import Database
from os.path import join

ip = '127.0.0.1'
port = '9010'
rate = 0.5 # measure data every x seconds
start_offset = 5
path_data = "data"
scheduler = sched.scheduler(time.time,
                            time.sleep)

class Measurement():
    def __init__(self, path_prgram: str) -> None:
        self.program = hp.read_json(path_prgram)
        self.bd = Database()
        self.current_step = "prolog"
        self.run_loop()
    

    def start(self):
        response  = requests.get(f'http://{ip}:{port}/start').json()
        if response['state'] != 'started':
            exit()
        self.add_task_setter() # important -> firt execute add tast setter
        self.add_task_getter()

    def stop(self):
        response  = requests.get(f'http://{ip}:{port}/stop').json()
        # print(response)


    def add_task_setter(self):
        start = start_offset
        for step in self.program:
            scheduler.enter(start, 1, self.set_data, (self.program[step], ))
            start += self.program[step]['duration']
        self.endtime = start + time.time()

    def add_task_getter(self):
        self.get_data()
        if time.time()< self.endtime:
            scheduler.enter(rate, 1, self.add_task_getter)

    def get_data(self):
        remeaning_time = self.endtime - time.time()
        print(f'remeaning time: {remeaning_time}')
        response = requests.get(f'http://{ip}:{port}/get_data').json()
        response["step_id"] = self.current_step
        self.bd.write_data(response)
        # print(response)

    def set_data(self, data:dict):
        self.current_step = data['id']
        print(f'setting data: {self.current_step}')
        requests.post(f'http://{ip}:{port}/set_data', json=data)


    def run_loop(self):
        self.start()
        scheduler.run()
        self.bd.data_to_csv(join(hp.create_folder("data"), "data.csv"))
        self.stop()
        