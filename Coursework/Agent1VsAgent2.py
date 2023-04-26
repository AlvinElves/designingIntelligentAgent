import time
import pandas as pd

from gym_xiangqi.agents import RandomAgent
from gym_xiangqi.constants import (     # NOQA
    RED, BLACK, PIECE_ID_TO_NAME, ALLY, ENEMY, ALIVE, DEAD
)
from gym_xiangqi.utils import action_space_to_move
from gym_xiangqi.envs import XiangQiEnv

from Agents.MiniMaxAgent import *
from Agents.AlphaBetaPruning import *
from Agents.MonteCarloTreeSearch import *

from QuestionFunctions import time_taken, movement_counter


def single_experiment(visualise, agent1, agent2):
    # Check which agents play to allow multiple experiment
    agent_player1 = starting_agent(agent1)
    agent_player2 = starting_agent(agent2)

    # Pass in the color you want to play as (RED or BLACK)
    env = XiangQiEnv(RED)
    if visualise:
        render_env = deepcopy(env)
        render_env.render()

    # Initialise the starting variables for each game
    done = False
    round_number = 0
    time_list = [[], []]
    chess_list = []

    # Put the list of chess movement into dataframe
    for i in range(len(PIECE_ID_TO_NAME)):
        chess_list.append([PIECE_ID_TO_NAME[i], 0, 0])

    piece_move_df = pd.DataFrame(chess_list, columns=['chess_piece', 'agent1_move', 'agent2_move'])

    while not done:
        # Initialise the starting variables for each round
        start_time = time.time()
        piece_list = []

        if env.turn == ALLY:
            # Check which agent plays to allow multiple experiment
            action, player = agent_moves(env, agent1, agent_player1, ALLY)

            _, reward, done, _ = env.step(action)
            if visualise:
                _, reward, done, _ = render_env.step(action)

            move = action_space_to_move(action)

            # Calculate the time taken for each actions
            time_list = time_taken(start_time, time.time(), time_list, ALLY)

            # Increase the counter based on the piece moved
            movement_counter(piece_move_df, PIECE_ID_TO_NAME[move[0]], ALLY)

            # Get the red pieces that are alive
            piece_set = env.ally_piece
            for piece_id, piece_obj in enumerate(piece_set[1:], 1):
                if piece_obj.state == ALIVE:
                    piece_list.append(PIECE_ID_TO_NAME[piece_id])

        else:
            # Check which agent plays to allow multiple experiment
            action, player = agent_moves(env, agent2, agent_player2, ENEMY)

            _, reward, done, _ = env.step(action)
            if visualise:
                _, reward, done, _ = render_env.step(action)

            move = action_space_to_move(action)

            # Calculate the time taken for each actions
            time_list = time_taken(start_time, time.time(), time_list, ENEMY)

            # Increase the counter based on the piece moved
            movement_counter(piece_move_df, PIECE_ID_TO_NAME[move[0]], ENEMY)

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
        print(f"{player} made the move {PIECE_ID_TO_NAME[move[0]]} from {move[1]} to {move[2]}.")
        print(f"Reward: {reward}")
        print("================")

        # If the round is over 200, then the game will be terminated and both of them drew
        if round_number >= 200 and not done:
            print("Resulting in Draw, Exceeded Round Limit")
            break

    print("Closing Xiangqi environment\n")
    env.close()
    return time_list


def agent_moves(env, agent, agent_player, player):
    if agent == 'random_agent':
        action = agent_player.move(env)
        player = "Random Agent"

    elif agent == 'minimax_agent':
        action = agent_player.minimax_N(env, 2)
        player = "Minimax Agent"

    elif agent == 'alpha_beta_agent':
        action = agent_player.alpha_beta_pruning_move(env, 2, player, 5)
        player = "Alpha Beta Agent"

    else:
        agent_player.update(env)
        original_state = env.state
        agent_player.montecarlo.simulate(100)
        chose_node = agent_player.montecarlo.make_choice()

        action = agent_player.find_move_action(original_state, chose_node.state.state)
        player = "Monte Carlo Agent"

    return action, player


def starting_agent(agent):
    if agent == 'random_agent':
        return RandomAgent()
    elif agent == 'minimax_agent':
        return MiniMaxAgent()
    elif agent == 'alpha_beta_agent':
        return AlphaBetaPruning()
    else:
        return MonteCarloTreeSearch()


if __name__ == '__main__':
    single_experiment(False, 'alpha_beta_agent', 'random_agent')
