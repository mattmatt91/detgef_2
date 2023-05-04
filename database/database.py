import sqlite3
import csv
from datetime import datetime
from random import randint
from time import sleep

keys = ['timestamp',
        'voltage',
        'current',
        'res_1',
        'res_2',
        'res_3',
        'res_4',
        "flow_mfc1",
        "flow_mfc2",
        "flow_mfc3",
        "flow_mfc4",
        "relais1",
        "relais2",
        "relais3",
        "relais4"
        ]


class Database():
    def __init__(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        sql_anweisung = """
        CREATE TABLE IF NOT EXISTS data_measurement (
        step_id TEXT,
        timestamp TEXT,
        voltage REAL,
        current REAL,
        res_1 INTEGER,
        res_2 INTEGER,
        res_3 INTEGER,
        res_4 INTEGER,
        flow_mfc1 REAL,
        flow_mfc2 REAL,
        flow_mfc3 REAL,
        flow_mfc4 REAL,
        relais1 INTERGER,
        relais2 INTERGER,
        relais3 INTERGER,
        relais4 INTERGER 
        );"""

        cursor.execute(sql_anweisung)
        connection.commit()
        connection.close()

    def write_data(self, data: dict):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        new_data = (
            data["step_id"],
            data["timestamp"],
            data["voltage"],
            data["current"],
            data["res_1"],
            data["res_2"],
            data["res_3"],
            data["res_4"],
            data["flow_mfc1"],
            data["flow_mfc2"],
            data["flow_mfc3"],
            data["flow_mfc4"],
            data["relais1"],
            data["relais2"],
            data["relais3"],
            data["relais4"]
        )

        cursor.execute("""
                INSERT INTO data_measurement 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, new_data)

        connection.commit()
        connection.close()

    def read_data(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM data_measurement")
        content = cursor.fetchall()
        connection.close()
        return content

    def delete_table(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        cursor.execute("DROP TABLE data_measurement")
        connection.commit()
    
    def data_to_csv(self, path:str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM data_measurement')
        col_names = [description[0] for description in cursor.description]
        with open(path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(col_names)
            csvwriter.writerows(cursor)
        self.delete_table()
        connection.close()

if __name__ == '__main__':
    database = Database()
    for i in range(10):
        data = {
            "step_id": "test_id",
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
        sleep(1)
        database.write_data(data)
    database.data_to_csv()
