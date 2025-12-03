from scratch_4 import seatCalculator
import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce

configs = [
    ("dhondt", 1, 0),
    ("dhondt", 2, 0),
    ("sainte lague", 1, 0),
    ("sainte lague", 2, 0),
    ("single const", 1, 0),
]

def col_name(method, seatRatio, cutoff):
    return f"{method} {seatRatio},{cutoff}"

seats_list = []
for method, ratio, cutoff in configs:
    kwargs = {"methods": (method,),
              "seatRatio": ratio,
              "cutoff": cutoff}
    s = seatCalculator(**kwargs)
    seats_list.append(s)

seats = reduce(lambda left, right: left.join(right, how="outer"), seats_list).fillna(0)
seats = seats.loc[~(seats < 3).all(axis=1)]

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(seats)

graph_cols = [col_name(m, r, c) for (m, r, c) in configs]
graph = seats[graph_cols]
graph = graph.loc[~(graph == 0).all(axis=1)]
graph.sort_values(by=graph.columns[0], ascending=False, inplace=True)
graph.plot(kind="bar")
plt.title("Spanish Election Results depending on the method/parliament size/cutoff used")
plt.xlabel("Parties in parliament")
plt.ylabel("# of seats won")
plt.show()
