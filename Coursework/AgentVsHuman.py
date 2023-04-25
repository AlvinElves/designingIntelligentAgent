import time

from gym_xiangqi.agents import RandomAgent
from gym_xiangqi.constants import (     # NOQA
    RED, BLACK, PIECE_ID_TO_NAME, ALLY, ENEMY, ALIVE, DEAD
)
from gym_xiangqi.utils import action_space_to_move
from gym_xiangqi.envs import XiangQiEnv

from Agents.MiniMaxAgent import *
from Agents.AlphaBetaPruning import *
from Agents.MonteCarloTreeSearch import *


def main_experiment(agent1, agent2):
    if agent1 == 'random_agent':
        random_agent = RandomAgent()
    elif agent1 == 'minimax_agent':
        minimax_agent = MiniMaxAgent()
    elif agent1 == 'alpha_beta_agent':
        alpha_beta_agent = AlphaBetaPruning()
    else:
        monte_carlo_agent = MonteCarloTreeSearch()

    if agent2 == 'random_agent':
        random_agent = RandomAgent()
    elif agent2 == 'minimax_agent':
        minimax_agent = MiniMaxAgent()
    elif agent2 == 'alpha_beta_agent':
        alpha_beta_agent = AlphaBetaPruning()
    else:
        monte_carlo_agent = MonteCarloTreeSearch()

    # Pass in the color you want to play as (RED or BLACK)
    env = XiangQiEnv(RED)
    render_env = deepcopy(env)
    render_env.render()

    done = False
    round_number = 0
    time_list = [[], []]

    while not done:
        start_time = time.time()
        piece_list = []

        if env.turn == ALLY:
            action = random_agent.move(env)
            player = "MonteCarlo Agent"

            _, reward, done, _ = env.step(action)
            _, reward, done, _ = render_env.step(action)

            move = action_space_to_move(action)

            piece = PIECE_ID_TO_NAME[move[0]]
            start = move[1]
            end = move[2]

            # Calculate the time taken for each actions
            end_time = time.time()
            difference = end_time - start_time
            time_list[0].append(difference)

            piece_set = env.ally_piece

            for piece_id, piece_obj in enumerate(piece_set[1:], 1):
                if piece_obj.state == ALIVE:
                    piece_list.append(PIECE_ID_TO_NAME[piece_id])

        else:
            monte_carlo_agent.update(env)
            original_state = env.state
            monte_carlo_agent.montecarlo.simulate(100)
            chose_node = monte_carlo_agent.montecarlo.make_choice()

            action = monte_carlo_agent.find_move_action(original_state, chose_node.state.state)
            player = "Random Agent"

            _, reward, done, _ = env.step(action)
            _, reward, done, _ = render_env.step(action)

            move = action_space_to_move(action)

            piece = PIECE_ID_TO_NAME[move[0]]
            start = move[1]
            end = move[2]

            # Calculate the time taken for each actions
            end_time = time.time()
            difference = end_time - start_time
            time_list[1].append(difference)

            piece_set = env.enemy_piece

            for piece_id, piece_obj in enumerate(piece_set[1:], 1):
                if piece_obj.state == ALIVE:
                    piece_list.append(PIECE_ID_TO_NAME[piece_id])

        render_env.render()

        round_number += 1
        print(f"Pieces Alive: {piece_list}")
        print(f"Round: {round_number}")
        print(f"{player} made the move {piece} from {start} to {end}.")
        print(f"Reward: {reward}")
        print("================")

    print("Closing Xiangqi environment")
    env.close()


if __name__ == '__main__':
    main_experiment('random_agent', 'monte_carlo_agent')
