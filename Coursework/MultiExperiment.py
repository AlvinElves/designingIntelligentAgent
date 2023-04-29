import numpy as np
import os

from Agent1VsAgent2 import single_experiment
from Visualisations import *


def multi_run_experiment(visualise, agent1, agent2):
    time_taken_df = pd.DataFrame()
    outcome_df = pd.DataFrame(columns=[agent1 + ' outcome'] + [agent2 + ' outcome'])
    dead_pieces_df = pd.DataFrame()
    chess_piece_df = pd.DataFrame()
    reward_df = pd.DataFrame()
    sacrifice_df = pd.DataFrame()
    for run in range(5):
        print(f"Run Number: {run + 1}, {agent1} VS {agent2}")
        list_of_result = single_experiment(visualise, agent1, agent2)
        run_number = 'run ' + str(run + 1)

        # Merge the time taken for each agent and run, side by side into a dataframe
        temp_df = pd.DataFrame()
        temp_df[agent1 + ' time taken ' + run_number] = list_of_result[0][0]
        time_taken_df = pd.merge(time_taken_df, temp_df, how='outer', left_index=True, right_index=True)

        temp_df = pd.DataFrame()
        temp_df[agent2 + ' time taken ' + run_number] = list_of_result[0][1]
        time_taken_df = pd.merge(time_taken_df, temp_df, how='outer', left_index=True, right_index=True)

        # Append the result of the game to the outcome dataframe
        outcome_df.loc[len(outcome_df)] = list_of_result[1]

        # merge the agent 1 dead pieces after the round ended, side by side into a dataframe
        temp_df = pd.DataFrame()
        temp_df[agent1 + ' dead pieces ' + run_number] = list_of_result[2]
        dead_pieces_df = pd.merge(dead_pieces_df, temp_df, how='outer', left_index=True, right_index=True)

        # merge the agent 2 dead pieces after the round ended, side by side into a dataframe
        temp_df = pd.DataFrame()
        temp_df[agent2 + ' dead pieces ' + run_number] = list_of_result[3]
        dead_pieces_df = pd.merge(dead_pieces_df, temp_df, how='outer', left_index=True, right_index=True)

        # merge the chess piece move, side by side into a dataframe
        list_of_result[4].columns = ['chess_piece', agent1 + ' moves ' + run_number, agent2 + ' moves ' + run_number]
        if run == 0:
            chess_piece_df = list_of_result[4]
        else:
            chess_piece_df = pd.merge(chess_piece_df, list_of_result[4], on='chess_piece')

        # Merge the reward for each agent and run, side by side into a dataframe
        temp_df = pd.DataFrame(list_of_result[5], columns=[agent1 + ' reward ' + run_number, agent2 + ' reward ' + run_number])
        reward_df = pd.merge(reward_df, temp_df, how='outer', left_index=True, right_index=True)

        # Merge the sacrifice piece for agent 1 each run, side by side into a dataframe
        if len(list_of_result[6][0]) == 0:  # If the list is empty
            list_of_result[6][0] = [np.nan, np.nan, np.nan]

        temp_df = pd.DataFrame()
        temp_df[[agent1 + ' round number ' + run_number, agent1 + ' sacrifice piece ' + run_number,
                agent1 + ' revenge piece ' + run_number]] = list_of_result[6][0]
        sacrifice_df = pd.merge(sacrifice_df, temp_df, how='outer', left_index=True, right_index=True)

        # Merge the sacrifice piece for agent 2 each run, side by side into a dataframe
        if len(list_of_result[6][1]) == 0:  # If the list is empty
            list_of_result[6][1] = [np.nan, np.nan, np.nan]
        temp_df = pd.DataFrame()
        temp_df[[agent2 + ' round number ' + run_number, agent2 + ' sacrifice piece ' + run_number,
                agent2 + ' revenge piece ' + run_number]] = list_of_result[6][1]
        sacrifice_df = pd.merge(sacrifice_df, temp_df, how='outer', left_index=True, right_index=True)

    return time_taken_df, outcome_df, dead_pieces_df, chess_piece_df, reward_df, sacrifice_df


def multi_agent_experiment(visualise):
    agents_list = ['random_agent', 'minimax_agent', 'alpha_beta_agent', 'monte_carlo_agent']
    sheet_column = ['Time_Taken', 'Outcome', 'Dead_Pieces', 'Moves_Pieces', 'Reward', 'Sacrifice_Pieces']
    directory_name = 'Results'

    # Create Folder Directory to store results
    try:
        os.mkdir(directory_name)
    except OSError as error:
        print(error)
    for agent1 in agents_list:
        for agent2 in agents_list:
            if agent1 != agent2:
                result_df = multi_run_experiment(visualise, agent1, agent2)
                file_name = directory_name + '/' + agent1 + 'VS' + agent2 + '.xlsx'

                with pd.ExcelWriter(file_name) as writer:
                    for i in range(len(result_df)):
                        result_df[i].to_excel(writer, sheet_name=sheet_column[i], index=False)


def read_results_file():
    agents_list = ['random_agent', 'minimax_agent', 'alpha_beta_agent', 'monte_carlo_agent']
    sheet_column = ['Time_Taken', 'Outcome', 'Dead_Pieces', 'Moves_Pieces', 'Reward', 'Sacrifice_Pieces']
    directory_name = 'Results'
    time_taken_list = []
    outcome_list = []
    dead_pieces_list = []
    chess_piece_list = []
    reward_list = []
    sacrifice_list = []

    for agent1 in agents_list:
        for agent2 in agents_list:
            if agent1 != agent2:
                file_name = directory_name + '/' + agent1 + 'VS' + agent2 + '.xlsx'

                time_taken_list.append(pd.read_excel(file_name, sheet_name=sheet_column[0]))
                outcome_list.append(pd.read_excel(file_name, sheet_name=sheet_column[1]))
                dead_pieces_list.append(pd.read_excel(file_name, sheet_name=sheet_column[2]))
                chess_piece_list.append(pd.read_excel(file_name, sheet_name=sheet_column[3]))
                reward_list.append(pd.read_excel(file_name, sheet_name=sheet_column[4]))
                sacrifice_list.append(pd.read_excel(file_name, sheet_name=sheet_column[5]))

    return time_taken_list, outcome_list, dead_pieces_list, chess_piece_list, reward_list, sacrifice_list


if __name__ == '__main__':
    #multi_agent_experiment(False)
    result_list = read_results_file()
    Visualisations(result_list)
