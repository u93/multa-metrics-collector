import pandas as pd
import datetime as dt
from Funciones import Statement_change
from Parametros import mylist

# Leemos el CSV y convertimos en dataframe
Uge = pd.read_csv(r"ElU.csv")
df = pd.DataFrame(Uge)

# Procesamos el df: convertimos timestamp a column time y date, y ordenamos el CSV
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
df = df.sort_values(by=["serial_number", "timestamp"])
df["tiempo"] = df["timestamp"]
df["tiempo"] = pd.to_datetime(df["tiempo"], format="H%:M%:S%").dt.time
df["fecha"] = df["timestamp"]
df["fecha"] = pd.to_datetime(df["fecha"], format="%d-%m-%y").dt.date
df["cambio_estado"] = 0

# Llamamos función de cambios de estados
Statement_change(
    df,
    parameter=mylist["Agent"],
    horainicio=mylist["Star_Time"],
    horafin=mylist["End_Time"],
    fechainicio=mylist["Star_Date"],
    fechafin=mylist["End_Date"],
)
