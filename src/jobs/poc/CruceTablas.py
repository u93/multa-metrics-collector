import pandas as pd
import numpy as np
from pandas import ExcelWriter

# BD1 = pd.ExcelFile("BD1.xlsx")
# df = BD1.parse("Hoja1")

BD1 = pd.read_excel(r"BD1.xlsx")
df = pd.DataFrame(BD1)
BD2 = pd.read_excel(r"BD2.xlsx")
df2 = pd.DataFrame(BD2)
df = df.set_index("Key")
df2 = df2.set_index("Key")
df.loc[df["Region"] == "Madrid", "Conform"] = 1
df.loc[df["Region"] == "Centro", "Conform"] = 1

Tabla_Cruce = pd.merge(df, df2, left_on="Key", right_on="Key", how="left")

Tabla_Cruce.loc[Tabla_Cruce["Precio"] < 100000, "+100mil"] = "- de cien"
Tabla_Cruce.loc[Tabla_Cruce["Precio"] > 100000, "+100mil"] = "+ de cien"
Tabla_Cruce["Intento"] = 0
# Nathalie = Tabla_Cruce.pivot_table(index='Region', columns='+100mil', values='Precio', aggfunc=sum)

Tabla_Cruce["Intento"] = Tabla_Cruce["Precio"] / Tabla_Cruce.groupby(Tabla_Cruce["Region"])["Precio"].transform("sum")
# Tabla_Cruce['Intento'] = Tabla_Cruce['Precio'].groupby(Tabla_Cruce['Region']).transform('sum')
# Tabla_Cruce.to_excel('C:/Users/jcort/Desktop/Test.xlsx', "Hoja1")

# df = df.drop(df.columns[[0,2]], axis=1)
# df.to_excel("BD1.xlsx", "Hoja1")

print(df)
print(df2)
print(Tabla_Cruce)
# print(Nathalie)
