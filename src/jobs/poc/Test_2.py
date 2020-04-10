import numpy as np
import pandas as pd
import datetime as dt

#organizamos el dataframe
Uge = pd.read_csv(r"ElU.csv")
df = pd.DataFrame(Uge)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit="s")
df = df.sort_values(by=['serial_number', 'timestamp'])
df['new'] = df['timestamp']
df['new'] = pd.to_datetime(df['new'], format='H%:M%:S%').dt.time
df = df[(df['new'] > dt.time(12,00,00)) & (df['new'] < dt.time(18,00,00))]

def activated(cajita, estado):

    Activity_box = df[df.serial_number == cajita][df.status == estado].count()['timestamp']

    return Activity_box

print(activated(input('Introduzca el dispositivo '), int(input('Introduzca el estado '))))








