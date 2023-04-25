from Agents.montecarlo.node import Node
from Agents.montecarlo.montecarlo import MonteCarlo

from copy import deepcopy
import numpy as np
from gym_xiangqi.constants import BOARD_ROWS, BOARD_COLS, ALLY, ALIVE, GENERAL
from gym_xiangqi.utils import move_to_action_space


class MonteCarloTreeSearch:
    def __init__(self):
        pass

    def update(self, env):
        self.montecarlo = MonteCarlo(Node(env))
        self.montecarlo.child_finder = self.child_finder
        self.montecarlo.node_evaluator = self.node_evaluator

    def child_finder(self, node):
        # get the list of legal moves
        actions = (node.state.ally_actions if node.state.turn == ALLY
                   else node.state.enemy_actions)
        legal_moves = np.where(actions == 1)[0]

        for move in legal_moves:
            child = Node(deepcopy(node.state))
            child.state.step(move)
            node.add_child(child)

    def node_evaluator(self, node):
        piece_set = node.state.ally_piece

        for piece_id, piece_obj in enumerate(piece_set[1:], 1):
            if piece_obj.state == ALIVE:
                if piece_id == GENERAL:
                    return 1
                else:
                    return -1

    # Find the action number from the original state and monte carlo chosen node state
    def find_move_action(self, original_state, action_state):
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if original_state[r][c] != action_state[r][c]:
                    if action_state[r][c] != 0:
                        print(action_state[r][c])
                        move_piece = abs(action_state[r][c])
                        end_pos = [r, c]
                    else:
                        start_pos = [r, c]

        return move_to_action_space(move_piece, start_pos, end_pos)
