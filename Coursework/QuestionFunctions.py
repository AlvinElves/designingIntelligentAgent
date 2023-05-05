# This File is created by myself
from gym_xiangqi.constants import ALLY, ALIVE, PIECE_ID_TO_NAME


def time_taken(start_time, end_time, time_list, player):
    difference = end_time - start_time

    if player == ALLY:
        time_list[0].append(difference)
    else:
        time_list[1].append(difference)

    return time_list


def check_sacrifice(original_list, pieces_list):
    sacrifice_list = list(set(original_list) - set(pieces_list))
    if len(sacrifice_list) == 0:
        sacrifice = False
    else:
        sacrifice = True

    return pieces_list, sacrifice, sacrifice_list


def sacrifice_pieces_ate(env, player, previous_piece_list):
    piece_list = alive_pieces(env, player)

    pieces_ate = list(set(previous_piece_list) - set(piece_list))

    if len(pieces_ate) == 0:
        return 'None'
    else:
        return pieces_ate[0]


def alive_pieces(env, player):
    piece_list = []
    if player == ALLY:
        piece_set = env.ally_piece
    else:
        piece_set = env.enemy_piece

    for piece_id, piece_obj in enumerate(piece_set[1:], 1):
        if piece_obj.state == ALIVE:
            piece_list.append(PIECE_ID_TO_NAME[piece_id])

    return piece_list


def dead_pieces(original_list, pieces_list):
    return list(set(original_list) - set(pieces_list))


def reward_counter(reward_list, reward_amount, player):
    if player == ALLY:
        if reward_amount != 0:
            reward_list.append([reward_amount, -reward_amount])
        else:
            reward_list.append([reward_amount, reward_amount])
    else:
        if reward_amount != 0:
            reward_list.append([-reward_amount, reward_amount])
        else:
            reward_list.append([reward_amount, reward_amount])

    return reward_list


def movement_counter(movement_dataset, piece, player):
    if player == ALLY:
        movement_dataset.loc[movement_dataset['chess_piece'] == piece, ['agent1_move']] = \
            movement_dataset.loc[movement_dataset['chess_piece'] == piece]['agent1_move'] + 1
    else:
        movement_dataset.loc[movement_dataset['chess_piece'] == piece, ['agent2_move']] = \
            movement_dataset.loc[movement_dataset['chess_piece'] == piece]['agent2_move'] + 1

