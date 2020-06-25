import numpy as np
import pandas as pd
import datetime as dt

# Uge = pd.read_csv(r"C:\Users\jcort\Desktop\ElU.csv")
Uge = pd.read_csv(r"ElU.csv")
df = pd.DataFrame(Uge)
# Uge = Uge.sort_values(by=['serial_number', 'timestamp'], ascending = [0, 0])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
df = df.sort_values(by=["serial_number", "timestamp"])

# for indice, fila in df.iterrows():
#   print(fila['serial_number'], fila['timestamp'], fila['status'])
# cantidad_fotos = df.groupby('serial_number')['timestamp'].count()


# Cajita = input()
# cantidad_fotos = df.groupby('serial_number')['timestamp'].count()[Cajita]

df["new"] = df["timestamp"]
df["new"] = pd.to_datetime(df["new"], format="H%:M%:S%").dt.time
df = df[(df["new"] > dt.time(12, 00, 00)) & (df["new"] < dt.time(18, 00, 00))]
# df = df.groupby('serial_number')['timestamp'].count()['080027526c42']
# df = df[df['serial_number'] == '080027526c42']
cant = df[df["status"] == 1].count()
cant2 = df[df["status"] == 0].count()

# cantidad_fotos = df.groupby(['serial_number', 'status']).count()[['new']]
# cantidad_fotos = df[df['serial_number'] == '080027526c42']
# cantidad_fotos = df[df.serial_number == 'test_local_sergio21'][df.status == 1].groupby(['serial_number', 'status']).count()[['new']]
# cantidad_fotos = df[df.serial_number == 'test_local_sergio21'][df.status == 1].count()
cantidad_fotos = df.groupby(["serial_number", "status"]).agg({"status": "count", "timestamp": ["first", max]})

# print(df[['serial_number', 'timestamp', 'status']].head(1000))

print(df[["serial_number", "status", "new"]])
print(cant["status"])
print(cant2["status"])
print(str(round(cant["status"] / (cant["status"] + cant2["status"]) * 100, 2)) + str(" %"))

print(cantidad_fotos)

topo = 6
