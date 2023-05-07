# This File is adapted from Xiangqi OpenAI Gym Environment
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

from QuestionFunctions import time_taken, movement_counter, reward_counter, dead_pieces, alive_pieces, check_sacrifice, sacrifice_pieces_ate


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
    piece_move_list = []

    # Put the list of chess movement into dataframe
    for i in range(len(PIECE_ID_TO_NAME)):
        piece_move_list.append([PIECE_ID_TO_NAME[i], 0, 0])

    piece_move_df = pd.DataFrame(piece_move_list, columns=['chess_piece', 'agent1_move', 'agent2_move'])

    reward_list = []
    sacrifice_list = [[], []]

    original_ally_pieces = alive_pieces(env, ALLY)
    original_enemy_pieces = alive_pieces(env, ENEMY)

    while not done:
        # Initialise the starting variables for each round
        start_time = time.time()

        if env.turn == ALLY:
            # Get the red pieces that are alive
            ally_piece_list = alive_pieces(env, ALLY)

            # Check if there is any sacrifice piece
            original_ally_pieces, ally_sacrifice, ally_sacrifice_list = check_sacrifice(original_ally_pieces, ally_piece_list)

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

            # Calculate the reward
            reward_counter(reward_list, reward, ALLY)

            # Check if you ate any piece after sacrifice
            if ally_sacrifice:
                piece_revenged = sacrifice_pieces_ate(env, ENEMY, original_enemy_pieces)
                sacrifice_list[0].append([round_number + 1, ally_sacrifice_list[0], piece_revenged])

            print(f"Pieces Alive: {ally_piece_list}")

        else:
            # Get the black pieces that are alive
            enemy_piece_list = alive_pieces(env, ENEMY)

            # Check if there is any sacrifice piece
            original_enemy_pieces, enemy_sacrifice, enemy_sacrifice_list = check_sacrifice(original_enemy_pieces, enemy_piece_list)

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

            # Calculate the reward
            reward_counter(reward_list, reward, ENEMY)

            # Check if you ate any piece after sacrifice
            if enemy_sacrifice:
                piece_revenged = sacrifice_pieces_ate(env, ALLY, original_ally_pieces)
                sacrifice_list[1].append([round_number + 1, enemy_sacrifice_list[0], piece_revenged])

            print(f"Pieces Alive: {enemy_piece_list}")

        if visualise:
            render_env.render()

        round_number += 1
        print(f"Round: {round_number}")
        print(f"{player} made the move {PIECE_ID_TO_NAME[move[0]]} from {move[1]} to {move[2]}.")
        print(f"Reward: {reward}")
        print("================")

        # If the round is over 200, then the game will be terminated and both of them drew
        if round_number >= 200 and not done:
            print("Resulting in Draw, Exceeded Round Limit")
            outcome = 'BOTH AGENT DRAW'
            outcome_list = ['Draw', 'Draw']
            break

        # if the round is over
        elif done:
            # If the current turn is enemy, then agent 1 won, since after ally move the game ended
            if env.turn == ENEMY:
                outcome = agent1 + ' WINS'
                outcome_list = ['Win', 'Lose']

            else:
                outcome = agent2 + ' WINS'
                outcome_list = ['Lose', 'Win']

    print(outcome)
    ally_dead_piece = dead_pieces(PIECE_ID_TO_NAME[1:], alive_pieces(env, ALLY))
    enemy_dead_piece = dead_pieces(PIECE_ID_TO_NAME[1:], alive_pieces(env, ENEMY))
    print("Closing Xiangqi environment\n")

    env.close()
    return time_list, outcome_list, ally_dead_piece, enemy_dead_piece, piece_move_df, reward_list, sacrifice_list


# Get the agent movement based on the decision made
def agent_moves(env, agent, agent_player, player):
    if agent == 'random_agent':
        action = agent_player.move(env)
        player = "Random Agent"

    elif agent == 'minimax_agent':
        action = agent_player.minimax_N(env, 2)
        player = "Minimax Agent"

    elif agent == 'alpha_beta_agent':
        action = agent_player.alpha_beta_pruning_move(env, 3, player, 5)
        player = "Alpha Beta Agent"

    else:
        agent_player.update(env)
        original_state = env.state
        agent_player.montecarlo.simulate(100)
        chose_node = agent_player.montecarlo.make_choice()

        action = agent_player.find_move_action(original_state, chose_node.state.state)
        player = "Monte Carlo Agent"

    return action, player


# Initialise the agents for the experiments conducted
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
    # Testing the single experiment
    round_result = single_experiment(True, 'alpha_beta_agent', 'random_agent')
