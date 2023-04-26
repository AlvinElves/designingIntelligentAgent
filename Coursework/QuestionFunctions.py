from gym_xiangqi.constants import ALLY


def time_taken(start_time, end_time, time_list, player):
    difference = end_time - start_time

    if player == ALLY:
        time_list[0].append(difference)
    else:
        time_list[1].append(difference)

    return time_list


def movement_counter(movement_dataset, piece, player):
    if player == ALLY:
        movement_dataset.loc[movement_dataset['chess_piece'] == piece, ['agent1_move']] = \
            movement_dataset.loc[movement_dataset['chess_piece'] == piece]['agent1_move'] + 1
    else:
        movement_dataset.loc[movement_dataset['chess_piece'] == piece, ['agent2_move']] = \
            movement_dataset.loc[movement_dataset['chess_piece'] == piece]['agent2_move'] + 1

