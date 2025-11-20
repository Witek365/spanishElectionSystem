import pandas as pd


def test_dhondt_allocation():
    # Sample votes data: parties as index, votes as values
    votes = pd.Series({'PartyA': 4*800, 'PartyB': 800, 'PartyC': 600})
    total_seats = 5

    # Initialize seats allocated with proper index
    seats_allocated = pd.Series(0, index=votes.index, dtype=int)

    # Copy votes for quotient calculations
    quotients = votes.copy()

    for _ in range(total_seats):
        max_party = quotients.idxmax()
        print(f"Allocating seat to: {max_party}")
        seats_allocated[max_party] += 1
        # Update quotient for the assigned party
        quotients[max_party] = votes[max_party] / (seats_allocated[max_party] + 1)

    print("Final seat allocation:")
    print(seats_allocated)


# Run the test
test_dhondt_allocation()
