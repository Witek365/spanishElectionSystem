from CalculatingSeats import seatCalculator
import pandas as pd
import matplotlib.pyplot as plt

seats = seatCalculator().join(seatCalculator(cutoff=0.05))
seats = seats.fillna(0)
seats = seats.loc[~(seats == 0).all(axis=1)]
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(seats)
graph = seats[["dhondt 1,0", "dhondt 1,0.05", "single const 1,0.05", "single const 1,0", "winner takes all 1,0"]]
graph = graph.loc[~(graph == 0).all(axis=1)]
graph.sort_values(by=graph.columns[0], ascending=False, inplace=True)
graph.plot(kind="bar")
plt.show()
