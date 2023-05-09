import schedule
from helpers import helpers as hp
import time
import requests
from datetime import datetime, timedelta
from database.database import Database
from os.path import join

ip = '127.0.0.1'
port = '9010'
rate = 10
start_offset = 5
path_data = "data"

class Measurement():
    def __init__(self, path_prgram: str) -> None:
        self.program = hp.read_json(path_prgram)
        self.bd = Database()
        self.add_schedule_get_data()
        self.add_schedule_set_data()
        self.current_step = "prolog"
        self.run_loop()
    

    def start(self):
        response  = requests.get(f'http://{ip}:{port}/start').json()
        print(response)

    def stop(self):
        response  = requests.get(f'http://{ip}:{port}/stop').json()
        print(response)

    def get_entire_duration(self):
        entire_duration = start_offset
        for step_id in self.program:
            entire_duration += self.program[step_id]["duration"]
        return entire_duration
    
    def add_schedule_get_data(self):
        schedule.every(rate).seconds.do(self.get_data)

    def add_schedule_set_data(self):
        start_time = datetime.now()
        sum_duration = start_offset
        for step_id in self.program:
            schedule_date_dt_obj = start_time + timedelta(seconds=sum_duration)
            schedule_date = schedule_date_dt_obj.strftime("%H:%M:%S")
            schedule.every().day.at(schedule_date).do(self.set_data, data= self.program[step_id])
            sum_duration += self.program[step_id]['duration']
            
    def get_data(self):
        response = requests.get(f'http://{ip}:{port}/get_data').json()
        response["step_id"] = self.current_step
        print(response)

    def set_data(self, data:dict):
        self.current_step = data['id']
        requests.post(f'http://{ip}:{port}/set_data', json=data)


    def run_loop(self):
        self.start()
        time.sleep(2)
        endtime = datetime.now() + timedelta(seconds=self.get_entire_duration())
        while endtime > datetime.now():
                schedule.run_pending()
                time.sleep(1)
                print(endtime-datetime.now())
        self.bd.data_to_csv(join(hp.create_folder("data"), "data.csv"))
        self.stop()
        