import numpy as np
import pandas as pd
import datetime as dt
from Parametros import End_Date

lectura = pd.read_csv(r"3568295d-5f24-45af-9b49-ac57cf9f4861.csv")
df1 = pd.DataFrame(lectura)
df1['timestamp'] = pd.to_datetime(df1['timestamp'], unit="s")
df1 = df1.sort_values(by=['serial_number', 'timestamp'])
df1['Date'] = df1['timestamp']
df1['Date'] = pd.to_datetime(df1['Date'], format='Y%:m%:d%').dt.date
df1['Time'] = df1['timestamp']
df1['Time'] = pd.to_datetime(df1['Time']).dt.time
df1 = df1[df1['serial_number'] == 'multa-agent-compose-6']

print(df1[['serial_number', 'timestamp']])
print(df1[['serial_number', 'timestamp']])