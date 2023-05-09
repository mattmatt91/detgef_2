
from time import sleep
import pandas as pd



class Database():
    def __init__(self):
        self.data = []


    def write_data(self, data: dict):
       self.data.append(data)

      
    
    def data_to_csv(self, path:str):
        df = pd.DataFrame(self.data)
        print(df)
        df.to_csv(path, decimal=',', sep=';', index=False)
      

if __name__ == '__main__':
    db = Database()
    for i in range(100):
        data = {'n':i, 'value':i*2, 'mybool':True}
        db.write_data(data)
    db.data_to_csv('test.txt')