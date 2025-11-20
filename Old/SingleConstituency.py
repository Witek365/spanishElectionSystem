import pandas as pd

def SingleConstituency(method, cutoff):

    df = pd.read_excel('G2023julio_mesas.xlsx', sheet_name='CCAA (OFICIALES)')


    valid_votes = df['VÁLIDOS']
    valid_sum = valid_votes.sum()
    autocomu_votes = df.iloc[:, 16:]
    national_votes = autocomu_votes.sum()





    def dhondt_allocation(votes: pd.Series, total_seats: int) -> pd.Series:

        parties = votes.index
        seats_allocated = pd.Series([0] * len(parties), index=parties)
        quotients = votes.copy()

        for _ in range(total_seats):
            # Find party with max quotient
            max_party = quotients.idxmax()
            # Allocate seat
            seats_allocated[max_party] += 1
            # Update quotient for that party
            quotients[max_party] = votes[max_party] / (seats_allocated[max_party] + 1)
            if _ % 100 == 0:
                print(quotients)

        return seats_allocated


    def sainLague_allocation(votes: pd.Series, total_seats: int) -> pd.Series:
        parties = votes.index
        seats_allocated = pd.Series([0] * len(parties), index=parties)
        quotients = votes.copy()

        for _ in range(total_seats):
            # Find party with max quotient
            max_party = quotients.idxmax()
            # Allocate seat
            seats_allocated[max_party] += 1
            # Update quotient for that party
            quotients[max_party] = votes[max_party] / (2 * seats_allocated[max_party] + 1)
            #if _%100 == 0:
            #print(quotients)

        return seats_allocated


    dhontsseats = dhondt_allocation(national_votes, 350)
    sainseats = sainLague_allocation(national_votes, 350)

    results = pd.DataFrame({"Dhondt": dhontsseats, "sainlague": sainseats})
    results = results[results['sainlague'] > 0]
    print(results)

    #Poland Like 5% Electoral Cutoff

    imp_parties = national_votes[national_votes >= sum(national_votes)*0.000005]
    print(imp_parties)
    res = dhondt_allocation(imp_parties,350)
    print(res[res>0])

if __name__ == "__main__":
    SingleConstituency(method='dhondt',cutoff=0)


