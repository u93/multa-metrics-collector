import numpy as np
import pandas as pd
import datetime as dt

lectura = pd.read_csv(r"3568295d-5f24-45af-9b49-ac57cf9f4861.csv")
df1 = pd.DataFrame(lectura)

print(df1[['serial_number', 'timestamp']])
print(df1[['serial_number', 'timestamp']])