import pandas as pd
from Provinces import df_seats_2023


#This Shows the American style of election: provinces are like states the winner takes all seats there
def seatCalculator(seatsRatio=1):
    excel_file = 'G2023julio_mesas.xlsx'

    df = pd.read_excel('G2023julio_mesas.xlsx', sheet_name='PROVINCIAS (OFICIALES)')
    df = pd.merge(df, df_seats_2023, on='PROVINCIA', how='outer')
    df = df.set_index('PROVINCIA')
    province_votes = df.iloc[:, 18:]


    def winnerTakesAll(row: pd.Series) -> pd.Series:
        total_seats = row['Congress_Seats_2023']
        votes = row.drop('Congress_Seats_2023')  # Extract votes by dropping seat count column
        seats_allocated = pd.Series(0, index=votes.index, dtype=int)
        max_party = votes.idxmax()
        seats_allocated[max_party] += total_seats

        return seats_allocated

    # Example applying on a DataFrame 'df' where last column is 'Congress_Seats_2023'
    result_df = province_votes.apply(winnerTakesAll, axis=1)
    resultSum = result_df.sum()
    print(resultSum[result_df > 0])
    return result_df


if __name__ == "__main__":
    seatCalculator()
