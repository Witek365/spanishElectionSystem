import pandas as pd
import numpy as np

def SeatAllocator(ratio):
    provinces = [
        "Almería", "Cádiz", "Córdoba", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla", "Huesca",
        "Teruel", "Zaragoza", "Asturias", "Illes Balears", "Las Palmas", "Santa Cruz de Tenerife",
        "Cantabria", "Albacete", "Ciudad Real", "Cuenca", "Guadalajara", "Toledo", "Ávila", "Burgos",
        "León", "Palencia", "Salamanca", "Segovia", "Soria", "Valladolid", "Zamora", "Barcelona",
        "Girona", "Lleida", "Tarragona", "Badajoz", "Cáceres", "A Coruña", "Lugo", "Ourense",
        "Pontevedra", "Madrid", "Navarra", "Araba / Álava", "Gipuzkoa", "Bizkaia", "Murcia", "La Rioja",
        "Alicante / Alacant", "Castellón / Castelló", "Valencia / València", "Ceuta", "Melilla"
    ]

    seats = np.array([
        6, 9, 6, 7, 5, 5, 11, 12, 3, 3, 7, 7, 8, 8, 7, 5, 4, 5, 3, 3, 6, 3, 4,
        4, 3, 4, 3, 2, 5, 3, 32, 6, 4, 6, 5, 4, 8, 4, 4, 7, 37, 5, 4, 6, 8, 10, 4, 12, 5, 16, 1, 1
    ]) * ratio

    # Ensure both lists have 52 entries
    assert len(provinces) == 52, "Province count should be 52."
    assert len(seats) == 52, "Seat count should be 52."

    df_seats_2023 = pd.DataFrame({
        'PROVINCIA': provinces,
        'Congress_Seats_2023': seats
    })

    #print(2*df_seats_2023.sort_values(by='Congress_Seats_2023', ascending=False))
    return df_seats_2023
