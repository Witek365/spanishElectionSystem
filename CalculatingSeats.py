import pandas as pd
import matplotlib.pyplot as plt
from Provinces import SeatAllocator


def seatCalculator(
        seatRatio=1,
        cutoff=0,
        localPlotter=False,
        methods=("dhondt", "sainte lague", "winner takes all", "single const"),
        year='G2016_mesas.xlsx'
):

    df = pd.read_excel("dataverse_files/" + year, sheet_name='PROVINCIAS (OFICIALES)')
    # Ensuring that the names of the headers match
    df.columns = df.columns.str.strip()
    df = df.iloc[:52]
    df['PROVINCIA'] = df['PROVINCIA'].apply(normalize_provincia)
    # Adding seats allocated to provinces to the df
    seats = SeatAllocator(seatRatio)
    seats['PROVINCIA'] = seats['PROVINCIA'].apply(normalize_provincia)
    df = pd.merge(df, seats, on='PROVINCIA', how='outer')

    #Adding
    df = df.set_index('PROVINCIA')
    nulos_idx = df.columns.get_loc("NULOS")
    province_votes = df.iloc[:, nulos_idx + 1:]

    province_votes = province_votes.drop("VOTOS.CANDIDATURAS", axis=1, errors='ignore')

    #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
     #   print(province_votes)

    if cutoff > 0:
        valid_votes = df['VÁLIDOS']
        votes_sum = province_votes[:-1].sum()
        labels = votes_sum.loc[votes_sum < valid_votes.sum() * cutoff].index
        labels = labels[:-1]
        province_votes = province_votes.drop(columns=labels)
        # print(province_votes)

    cols = {}
    if "dhondt" in methods:
        resdho = province_votes.apply(dhondt_allocation_row_with_seats, axis=1)
        resdhosum = resdho.sum() / seatRatio
        cols[str(year[1:5]) + " dhondt " + str(seatRatio) + "," + str(cutoff)] = resdhosum

    if "sainte lague" in methods:
        ressl = province_votes.apply(sainte_lague_row_with_seats, axis=1)
        resslsum = ressl.sum() / seatRatio
        cols[str(year[1:5]) + " sainte lague " + str(seatRatio) + "," + str(cutoff)] = resslsum

    if "winner takes all" in methods:
        reswta = province_votes.apply(winnerTakesAll, axis=1)
        reswtasum = reswta.sum() / seatRatio
        cols[str(year[1:5]) + " winner takes all " + str(seatRatio) + "," + str(cutoff)] = reswtasum

    if "single const" in methods:
        ressc = SingleConstituency(province_votes)
        cols[str(year[1:5]) + " single const " + str(seatRatio) + "," + str(cutoff)] = ressc

    sbs = pd.DataFrame(cols)

    sorter = str(year[1:5]) + " dhondt " + str(seatRatio) + "," + str(cutoff)

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



def normalize_provincia(provincia):
    """Map variant spellings to a standard name"""
    province_mapping = {
        # Accents and spacing variants
        "A Coruña": "A Corunya",
        "Almería": "Almeria",
        "Araba / Álava": "Araba / Alava",
        "Araba / alava": "Araba / Alava",
        "Cáceres": "Caceres",
        "Cádiz": "Cadiz",
        "Córdoba": "Cordoba",
        "Guipuzcoa": "Gipuzkoa",
        "Jaén": "Jaen",
        "León": "Leon",
        "Málaga": "Malaga",
        "Ávila": "Avila",
        "avila": "Avila",
        "Castellón / Castelló": "Castellon / Castello",  # Changed ó to ó
        "Valencia / València": "Valencia / Valencia"
    }
    return province_mapping.get(provincia, provincia)
if __name__ == "__main__":
    seatCalculator(localPlotter=True)
