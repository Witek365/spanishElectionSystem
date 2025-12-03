import pandas as pd
import matplotlib.pyplot as plt
from Provinces import SeatAllocator



def seatCalculator(
    seatRatio=1,
    cutoff=0,
    localPlotter=False,
    methods=("dhondt", "sainte lague", "winner takes all", "single const"),
):
    excel_file = 'G2023julio_mesas.xlsx'
    sheets = pd.ExcelFile(excel_file).sheet_names

    df = pd.read_excel('G2023julio_mesas.xlsx', sheet_name='PROVINCIAS (OFICIALES)')
    seats = SeatAllocator(seatRatio)
    df = pd.merge(df, seats, on='PROVINCIA', how='outer')

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #   print(df)

    df = df.set_index('PROVINCIA')
    province_votes = df.iloc[:, 18:]

    if cutoff > 0:
        valid_votes = df['VÁLIDOS']
        votes_sum = province_votes[:-1].sum()
        labels = votes_sum.loc[votes_sum < valid_votes.sum() * cutoff].index
        labels = labels[:-1]
        # print(labels)
        province_votes = province_votes.drop(columns=labels)
        # print(province_votes)

    # Example applying on a DataFrame 'df' where last column is 'Congress_Seats_2023'
    cols = {}
    if "dhondt" in methods:
        resdho = province_votes.apply(dhondt_allocation_row_with_seats, axis=1)
        resdhosum = resdho.sum() / seatRatio
        cols["dhondt " + str(seatRatio) + "," + str(cutoff)] = resdhosum

    if "sainte lague" in methods:
        ressl = province_votes.apply(sainte_lague_row_with_seats, axis=1)
        resslsum = ressl.sum() / seatRatio
        cols["sainte lague " + str(seatRatio) + "," + str(cutoff)] = resslsum

    if "winner takes all" in methods:
        reswta = province_votes.apply(winnerTakesAll, axis=1)
        reswtasum = reswta.sum() / seatRatio
        cols["winner takes all " + str(seatRatio) + "," + str(cutoff)] = reswtasum

    if "single const" in methods:
        ressc = SingleConstituency(province_votes)
        cols["single const " + str(seatRatio) + "," + str(cutoff)] = ressc

    sbs = pd.DataFrame(cols)

    sorter = "dhondt " + str(seatRatio) + "," + str(cutoff)

    if localPlotter and sorter in sbs.columns:
        sbsdrop = sbs.loc[~(sbs == 0).all(axis=1)]
        print(sbsdrop)

        sbsdrop.sort_values(by=sorter, ascending=False, inplace=True)
        sbsdrop.plot(kind="bar")
        plt.show()

    return sbs

def dhondt_allocation_row_with_seats(row: pd.Series) -> pd.Series:
    total_seats = row['Congress_Seats_2023']
    votes = row.drop('Congress_Seats_2023')  # Extract votes by dropping seat count column
    seats_allocated = pd.Series(0, index=votes.index, dtype=int)
    quotients = votes.copy()

    for _ in range(int(total_seats)):
        max_party = quotients.idxmax()
        seats_allocated[max_party] += 1
        quotients[max_party] = votes[max_party] / (seats_allocated[max_party] + 1)

    return seats_allocated

def sainte_lague_row_with_seats(row: pd.Series) -> pd.Series:
    total_seats = row['Congress_Seats_2023']
    votes = row.drop('Congress_Seats_2023')  # Extract votes by dropping seat count column
    seats_allocated = pd.Series(0, index=votes.index, dtype=int)
    quotients = votes.copy()

    for _ in range(int(total_seats)):
        max_party = quotients.idxmax()
        seats_allocated[max_party] += 1
        quotients[max_party] = votes[max_party] / (2 * seats_allocated[max_party] + 1)

    return seats_allocated

def winnerTakesAll(row: pd.Series) -> pd.Series:

    total_seats = row['Congress_Seats_2023']
    votes = row.drop('Congress_Seats_2023')  # Extract votes by dropping seat count column
    seats_allocated = pd.Series(0, index=votes.index, dtype=int)
    max_party = votes.idxmax()
    seats_allocated[max_party] += total_seats

    return seats_allocated

def SingleConstituency(data: pd.DataFrame, seatAllocation='dhondt') -> pd.Series:
    row = data.sum()
    if seatAllocation == 'dhondt':
        return dhondt_allocation_row_with_seats(row)
    if seatAllocation == 'sainte lague':
        return sainte_lague_row_with_seats(row)
    if seatAllocation == 'winner takes all':
        return winnerTakesAll(row)


if __name__ == "__main__":
    seatCalculator(localPlotter=True)
