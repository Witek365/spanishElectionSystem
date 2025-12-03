from CalculatingSeats import seatCalculator
import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce

#configs = [
#    ("G2016_mesas.xlsx", "dhondt", 1, 0),
#    ("G2023julio_mesas.xlsx", "dhondt", 2, 0),
#    ("G2023julio_mesas.xlsx", "sainte lague", 1, 0),
#    ("G2023julio_mesas.xlsx", "sainte lague", 2, 0),
#    ("G2023julio_mesas.xlsx", "single const", 1, 0),
#]
configs = [
    ("G2011_mesas.xlsx", "dhondt", 1, 0),
    ("G2015_mesas.xlsx", "dhondt", 1, 0),
    ("G2016_mesas.xlsx", "dhondt", 1, 0),
    ("G2019abril_mesas.xlsx", "dhondt", 1, 0),
]


def col_name(year, method, seatRatio, cutoff):
    return f"{year[1:5]} {method} {seatRatio},{cutoff}"


seats_list = []
for year, method, ratio, cutoff in configs:
    kwargs = {"year": year,
              "methods": (method,),
              "seatRatio": ratio,
              "cutoff": cutoff}
    print(kwargs)
    s = seatCalculator(**kwargs)
    seats_list.append(s)

seats = reduce(lambda left, right: left.join(right, how="outer"), seats_list).fillna(0)
seats = seats.loc[~(seats < 3).all(axis=1)]

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(seats)

graph_cols = [col_name(y, m, r, c) for (y, m, r, c) in configs]
graph = seats[graph_cols]
graph = graph.loc[~(graph == 0).all(axis=1)]
#print(sum(graph))
graph.sort_values(by=graph.columns[0], ascending=False, inplace=True)
graph.plot(kind="bar")
plt.title("Spanish Election Results depending on the method/parliament size/cutoff used")
plt.xlabel("Parties in parliament")
plt.ylabel("# of seats won")
plt.xticks(rotation=45, ha='right', fontsize=6)
plt.show()
