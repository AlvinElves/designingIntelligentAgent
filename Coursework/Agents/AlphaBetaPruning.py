import numpy as np
from copy import deepcopy

from gym_xiangqi.constants import BOARD_ROWS, BOARD_COLS, ALLY, PIECE_POINTS


class AlphaBetaPruning:
    def __init__(self):
        pass

    # Recursive alpha beta pruning function
    def alpha_beta_pruning_N(self, env, depth, alpha, beta):
        if depth == 0:
            return self.eval_board(env) + self.eval_space(env)

        # get the list of legal moves
        actions = (env.ally_actions if env.turn == ALLY
                   else env.enemy_actions)
        legal_moves = np.where(actions == 1)[0]

        if env.turn == ALLY:
            bestMove = -9999
            # score for each legal_moves
            for move in legal_moves:
                # copy the environment to avoid changing  the original environment
                temp = deepcopy(env)

                _, reward, done, _ = temp.step(move)

        else:
            bestMove = 9999

    # Get the best moves from the legal moves
    def alpha_beta_pruning_move(self, env, depth):
        # get the list of legal moves
        actions = (env.ally_actions if env.turn == ALLY
                   else env.enemy_actions)
        legal_moves = np.where(actions == 1)[0]

        bestMove = -9999
        bestMoveFinal = None

        # score for each legal_moves
        for move in legal_moves:
            # copy the environment to avoid changing  the original environment
            temp = deepcopy(env)

            _, reward, done, _ = temp.step(move)

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
