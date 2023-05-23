import pandas as pd


df = pd.read_csv('data\\05_15_2023-17_05_15\\data.csv')
df[['S2', 'S3', 'S4']].plot().show()
