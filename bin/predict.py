import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

processed_data = pd.read_csv('../data/processed/processed_dataset.csv')


def knn(name):
    """Use knn classifier on dataset for access to attribute kneighbors. Exact class of player is not important.
    That way we can get 10 most similar players to a given player by just printing out kneighbors attribute"""
    neigh = KNeighborsClassifier(n_neighbors=11)

    test = processed_data[(processed_data.Name == name)]
    if len(test) == 0:
        raise NameError('Player with that name does not exist!')

    same_position_players = processed_data[processed_data.Position == test.Position.iloc[0]]
    neigh.fit(same_position_players.drop(['Name', 'Value'], axis=1), same_position_players['Body Type'])
    res = neigh.kneighbors(test.drop(['Name', 'Value'], axis=1))

    for i in res[1]:
        players = same_position_players.iloc[i].Name
        players = players[players.map(lambda x: x != name)]

        for j in range(0, len(players)):
            print(j+1, ':', players.iloc[j])


if __name__ == '__main__':
    player = input('\nType in player name (q for exit): ')

    while player != 'q':
        try:
            knn(player)
        except NameError as err:
            print(err)
        except:
            print('Unexpected error!')

        player = input('\nType in player name (q for exit): ')
