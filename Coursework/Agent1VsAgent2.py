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


def single_experiment(visualise, agent1, agent2):
    # Check which agents play to allow multiple experiment
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
    if visualise:
        render_env = deepcopy(env)
        render_env.render()

    done = False
    round_number = 0
    time_list = [[], []]

    while not done:
        start_time = time.time()
        piece_list = []

        if env.turn == ALLY:
            # Check which agent plays to allow multiple experiment
            if agent1 == 'random_agent':
                action = random_agent.move(env)
                player = "Random Agent"

            elif agent1 == 'minimax_agent':
                action = minimax_agent.minimax_N(env, 2)
                player = "Minimax Agent"

            elif agent1 == 'alpha_beta_agent':
                action = alpha_beta_agent.alpha_beta_pruning_move(env, 3, ALLY, 5)
                alpha_beta_agent = AlphaBetaPruning()
                player = "Alpha Beta Agent"

            else:
                monte_carlo_agent.update(env)
                original_state = env.state
                monte_carlo_agent.montecarlo.simulate(100)
                chose_node = monte_carlo_agent.montecarlo.make_choice()

                action = monte_carlo_agent.find_move_action(original_state, chose_node.state.state)
                player = "Monte Carlo Agent"

            _, reward, done, _ = env.step(action)
            if visualise:
                _, reward, done, _ = render_env.step(action)

            move = action_space_to_move(action)

            piece = PIECE_ID_TO_NAME[move[0]]
            start = move[1]
            end = move[2]

            # Calculate the time taken for each actions
            end_time = time.time()
            difference = end_time - start_time
            time_list[0].append(difference)

            # Get the red pieces that are alive
            piece_set = env.ally_piece
            for piece_id, piece_obj in enumerate(piece_set[1:], 1):
                if piece_obj.state == ALIVE:
                    piece_list.append(PIECE_ID_TO_NAME[piece_id])

        else:
            # Check which agent plays to allow multiple experiment
            if agent2 == 'random_agent':
                action = random_agent.move(env)
                player = "Random Agent"

            elif agent2 == 'minimax_agent':
                action = minimax_agent.minimax_N(env, 2)
                player = "Minimax Agent"

            elif agent2 == 'alpha_beta_agent':
                action = alpha_beta_agent.alpha_beta_pruning_move(env, 3, ENEMY, 5)
                alpha_beta_agent = AlphaBetaPruning()
                player = "Alpha Beta Agent"

            else:
                monte_carlo_agent.update(env)
                original_state = env.state
                monte_carlo_agent.montecarlo.simulate(100)
                chose_node = monte_carlo_agent.montecarlo.make_choice()

                action = monte_carlo_agent.find_move_action(original_state, chose_node.state.state)
                player = "Monte Carlo Agent"

            _, reward, done, _ = env.step(action)
            if visualise:
                _, reward, done, _ = render_env.step(action)

            move = action_space_to_move(action)

            piece = PIECE_ID_TO_NAME[move[0]]
            start = move[1]
            end = move[2]

            # Calculate the time taken for each actions
            end_time = time.time()
            difference = end_time - start_time
            time_list[1].append(difference)

            # Get the black pieces that are alive
            piece_set = env.enemy_piece
            for piece_id, piece_obj in enumerate(piece_set[1:], 1):
                if piece_obj.state == ALIVE:
                    piece_list.append(PIECE_ID_TO_NAME[piece_id])

        if visualise:
            render_env.render()

        round_number += 1
        print(f"Pieces Alive: {piece_list}")
        print(f"Round: {round_number}")
        print(f"{player} made the move {piece} from {start} to {end}.")
        print(f"Reward: {reward}")
        print("================")

        # If the round is over 200, then the game will be terminated and both of them drew
        if round_number >= 200 and not done:
            print("Resulting in Draw, Exceeded Round Limit")
            break

    print("Closing Xiangqi environment\n")
    env.close()


if __name__ == '__main__':
    single_experiment('random_agent', 'monte_carlo_agent')
