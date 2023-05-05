# This File is created by myself
import numpy as np
from copy import deepcopy
import random

from gym_xiangqi.constants import BOARD_ROWS, BOARD_COLS, ALLY, PIECE_POINTS


class MiniMaxAgent:
    def __init__(self):
        pass

    # Recursive minimax function
    def minimax_N(self, env, depth):
        # get the list of legal moves
        actions = (env.ally_actions if env.turn == ALLY
                   else env.enemy_actions)
        legal_moves = np.where(actions == 1)[0]
        scores = []

        # score for each legal_moves
        for move in legal_moves:
            # copy the environment to avoid changing the original environment
            temp = deepcopy(env)
            _, reward, done, _ = temp.step(move)

            # if checkmate
            if temp.check_jiang():
                # Increased the score by 3 since checkmate is important
                scores.append(self.eval_board(temp) + 3)

            # if the game did not finish
            elif done is False:
                # if we have not got to the last depth
                if depth > 1:
                    temp_best_move = self.minimax_N(temp, depth - 1)
                    _, reward, done, _ = temp.step(temp_best_move)

                scores.append(self.eval_board(temp))

            # if the game finished from one of the move
            else:
                scores.append(self.eval_board(temp))

            # this is the secondary evaluation function
            scores[-1] = scores[-1] + self.eval_space(temp)

        # If the playing as red, use max score, playing as black, use min score
        if env.turn == ALLY:
            # Get the maximum score
            max_scores = max(scores)
            # Put the indexes of maximum score in a list
            max_list = [i for i, x in enumerate(scores) if x == max_scores]

            # Randomly choose from the list to explore more maximum score options
            best_move = legal_moves[random.choice(max_list)]
        else:
            # Get the minimum score
            min_scores = min(scores)
            # Put the indexes of minimum score in a list
            min_list = [i for i, x in enumerate(scores) if x == min_scores]

            # Randomly choose from the list to explore more minimum score options
            best_move = legal_moves[random.choice(min_list)]

        return best_move

    # Evaluate the score based on pieces on board
    def eval_board(self, env):
        score = 0
        current_board = env.state
        # Loop through the current board state to calculate the score
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                # If the piece is enemy
                if current_board[r][c] < 0:
                    # Minus score if enemy
                    score -= PIECE_POINTS[-current_board[r][c]]

                # If the piece is ally
                elif current_board[r][c] > 0:
                    # Add score if ally
                    score += PIECE_POINTS[current_board[r][c]]

        return score

    # Evaluate based on moves that can make the pieces position better
    def eval_space(self, env):
        # Get the legal moves based on the current states
        actions = (env.ally_actions if env.turn == ALLY
                   else env.enemy_actions)
        legal_moves = np.where(actions == 1)[0]

        # Get the number of moves
        number_of_moves = len(legal_moves)

        # Determine the value between 0 and 1, The 20 value is arbitrary but is chosen as it centers value around 0.5
        value = (number_of_moves / (20 + number_of_moves))

        # If red piece movement, return positive value
        if env.turn == ALLY:
            return value
        else:
            return -value
