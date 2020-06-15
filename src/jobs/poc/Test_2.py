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
df['fecha'] = df['timestamp']
df['fecha'] = pd.to_datetime(df['fecha'], format='%d-%m-%y').dt.date
#df = df[(df['new'] > dt.time(12,00,00)) & (df['new'] < dt.time(18,00,00))]
df['new2'] = 0
#df = df[df['serial_number'] == 'testEugenio-local']
#def activated(cajita, estado):

    #Activity_box = df[df.serial_number == cajita][df.status == estado].count()['timestamp']

    #return Activity_box
#print(activated(input('Introduzca el dispositivo '), int(input('Introduzca el estado '))))
print(len(df))
d=4

#FUNCION PARA CAMBIOS DE ESTADO
serieNo = input('Introduzca el dispositivo ')
df = df[df['serial_number'] == serieNo]
def Statement_change():

    for i in range(1, len(df)):
        if df.status.iloc[i] != df.status.iloc[i-1]:
            df.new2.iloc[i] = 1

    return print(df[['serial_number', 'status', 'fecha', 'new2', 'new']].head(40)), print(sum(df['new2']))

Statement_change()

