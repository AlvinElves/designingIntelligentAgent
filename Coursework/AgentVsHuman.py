import time

from gym_xiangqi.agents import RandomAgent
from gym_xiangqi.constants import (     # NOQA
    RED, BLACK, PIECE_ID_TO_NAME, ALLY, ENEMY
)
from gym_xiangqi.utils import action_space_to_move
from gym_xiangqi.envs import XiangQiEnv

from Agents.MiniMaxAgent import *
from Agents.AlphaBetaPruning import *


def main():
    # Pass in the color you want to play as (RED or BLACK)
    env = XiangQiEnv(BLACK)
    render_env = deepcopy(env)
    render_env.render()

    random_agent = RandomAgent()
    minimax_agent = MiniMaxAgent()
    alpha_beta_agent = AlphaBetaPruning()

    done = False
    round_number = 0

    while not done:
        if env.turn == ALLY:
            action = alpha_beta_agent.alpha_beta_pruning_move(env, 3, env.turn)

            _, reward, done, _ = env.step(action)
            _, reward, done, _ = render_env.step(action)

            player = "Alpha Beta Agent"
            move = action_space_to_move(action)

            piece = PIECE_ID_TO_NAME[move[0]]
            start = move[1]
            end = move[2]
        else:
            action = random_agent.move(env)

            _, reward, done, _ = env.step(action)
            _, reward, done, _ = render_env.step(action)

            player = "Random Agent"
            move = action_space_to_move(action)

            piece = PIECE_ID_TO_NAME[move[0]]
            start = move[1]
            end = move[2]

        render_env.render()

        round_number += 1
        print(f"Round: {round_number}")
        print(f"{player} made the move {piece} from {start} to {end}.")
        print(f"Reward: {reward}")
        print("================")

    print("Closing Xiangqi environment")
    env.close()


if __name__ == '__main__':
    main()
