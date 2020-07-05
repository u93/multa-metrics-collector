from datetime import datetime, date, time
import datetime as dt

# Función de cambios de estados con parámetros incorporados


def Statement_change(bbdd, parameter=None, horainicio=None, horafin=None, fechainicio=None, fechafin=None):

    # Filtramos por parámetros en caso de que haya
    if parameter != None:
        bbdd = bbdd[bbdd["serial_number"] == parameter]

    # Agregamos la librería dt para el filtro por tiempo
    if horainicio != None or horafin != None:
        bbdd = bbdd[
            (bbdd["tiempo"] > dt.datetime.strptime(horainicio, "%H:%M:%S").time())
            & (bbdd["tiempo"] < dt.datetime.strptime(horafin, "%H:%M:%S").time())
        ]

    # Agregamos la librería dt para el filtro por fecha
    if fechainicio != None or fechafin != None:
        bbdd = bbdd[
            (bbdd["fecha"] > dt.datetime.strptime(fechainicio, "%Y-%m-%d").date())
            & (bbdd["fecha"] < dt.datetime.strptime(fechafin, "%Y-%m-%d").date())
        ]

    # Bucle para determinar cantidad de cambios de estados
    for i in range(1, len(bbdd)):
        if bbdd.status.iloc[i] != bbdd.status.iloc[i - 1]:
            bbdd.cambio_estado.iloc[i] = 1

    return (
        print(bbdd[["serial_number", "status", "tiempo", "cambio_estado", "fecha"]].head(40)),
        print(bbdd[bbdd["cambio_estado"] == 1][["cambio_estado", "status", "tiempo", "fecha"]]),
        print(sum(bbdd["cambio_estado"])),
    )
