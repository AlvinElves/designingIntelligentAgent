# This File is created by myself
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

from gym_xiangqi.constants import PIECE_ID_TO_NAME


class Visualisations:
    def __init__(self, result_list):
        self.agents_list = ['random_agent', 'minimax_agent', 'alpha_beta_agent', 'monte_carlo_agent']
        time_taken_list = result_list[0]
        outcome_list = result_list[1]
        dead_pieces_list = result_list[2]
        chess_piece_list = result_list[3]
        reward_list = result_list[4]
        sacrifice_list = result_list[5]

        self.trace_name = ["Game 1", "Game 2", "Game 3", "Game 4",
                           "Game 5",
                           "Game 6", "Game 7", "Game 8", "Game 9",
                           "Game 10"]

        self.matches_order = self.agent_matches()

        self.movement_visualisation(chess_piece_list, self.matches_order, self.trace_name)
        self.total_movement_visualisation(chess_piece_list, self.matches_order, self.agents_list)
        self.dead_pieces_visualisation(dead_pieces_list, self.matches_order, self.trace_name)
        self.total_dead_piece_visualisation(dead_pieces_list, self.matches_order, self.agents_list)
        self.time_taken_visualisation(time_taken_list, self.matches_order, self.trace_name)
        self.total_time_taken_visualisation(time_taken_list, self.matches_order)
        self.reward_visualisation(reward_list, self.matches_order, self.trace_name)
        self.total_reward_visualisation(reward_list, self.matches_order)
        self.revenge_visualisation(sacrifice_list, self.matches_order, self.trace_name)
        self.total_revenge_visualisation(sacrifice_list, self.matches_order)
        self.win_rate_visualisation(outcome_list)

    # Get the order of the matches between the agents
    def agent_matches(self):
        matches_order = []
        for agent1 in self.agents_list:
            for agent2 in self.agents_list:
                if agent1 == agent2:
                    pass
                else:
                    matches_order.append([agent1, agent2])
        return matches_order

    # Visualising how many times does the agent sacrifice a piece to kill the opponent piece
    def total_revenge_visualisation(self, sacrifice_list, matches_order):
        agent_shown = []
        revenged_column = []
        game_column = []
        matches = []
        y_value = []

        # Loop through the agents
        for agent1 in self.agents_list:
            for agent2 in self.agents_list:
                if agent1 == agent2:
                    pass
                else:
                    # Merge the agents together if they are versing the same agents, just might be playing as red or black piece
                    if [agent1, agent2] and [agent2, agent1] not in agent_shown:
                        matches.append(matches_order.index([agent1, agent2]))
                        agent_shown.append([agent1, agent2])
                        matches.append(matches_order.index([agent2, agent1]))
                        agent_shown.append([agent2, agent1])

                    else:
                        continue

        # Create the figure
        fig = go.Figure()

        # Create the X Axis Label
        for i in range(len(agent_shown)):
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            revenged_column.extend([agent_shown[i][0] + ' No Revenge', agent_shown[i][0] + ' Revenged',
                                    agent_shown[i][1] + ' No Revenge', agent_shown[i][1] + ' Revenged'])

        x_axis_label = [game_column, revenged_column]
        print(x_axis_label)

        # Loop through the matches
        for i in range(len(agent_shown)):
            match = sacrifice_list[matches[i]]
            agent1_revenge = 0
            agent1_no_revenge = 0
            agent2_revenge = 0
            agent2_no_revenge = 0

            # Loop through the games
            for column in range(0, 30, 6):
                agent1_match = match[match.columns[column + 2]].dropna()
                agent2_match = match[match.columns[column + 5]].dropna()

                for row in range(len(agent1_match)):
                    if agent1_match.iloc[row] == 'None':
                        agent1_no_revenge += 1
                    else:
                        agent1_revenge += 1

                for row in range(len(agent2_match)):
                    if agent2_match.iloc[row] == 'None':
                        agent2_no_revenge += 1
                    else:
                        agent2_revenge += 1

            # Get the Y Values
            y_value.extend([agent1_no_revenge, agent1_revenge, agent2_no_revenge, agent2_revenge])

        # Create the Bar Figure
        fig.add_bar(x=x_axis_label, y=y_value)
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(xaxis=dict(tickfont=dict(size=10)), xaxis_title="Matches",
                          yaxis_title="Number of Chess Piece Revenged",
                          title="Chess Piece Revenge after Sacrificing Ally Chess Piece Experiments for the Agents")
        fig.show()

    # Visualising what piece did the agent killed after sacrificing a piece
    def revenge_visualisation(self, sacrifice_list, matches_order, trace_name):
        agent_shown = []
        revenge_piece = [['None', 0, 0]]
        # Put the list of dead pieces into list
        for i in range(1, len(PIECE_ID_TO_NAME)):
            revenge_piece.append([PIECE_ID_TO_NAME[i], 0, 0])

        # Create the empty dead pieces dataframe
        revenge_piece_df = pd.DataFrame(revenge_piece, columns=['chess_piece', 'agent1', 'agent2'])

        # Loop through the agents
        for agent1 in self.agents_list:
            for agent2 in self.agents_list:
                matches = []
                if agent1 == agent2:
                    pass
                else:
                    # Merge the agents together if they are versing the same agents, just might be playing as red or black piece
                    if [agent1, agent2] and [agent2, agent1] not in agent_shown:
                        matches.append(matches_order.index([agent1, agent2]))
                        agent_shown.append([agent1, agent2])
                        matches.append(matches_order.index([agent2, agent1]))
                        agent_shown.append([agent2, agent1])
                    else:
                        continue

                    # Initialise the variables
                    column_name = revenge_piece_df['chess_piece']
                    agent_column = []
                    piece_column = []

                    # Get the X axis label for the graph
                    for i in range(len(column_name.values)):
                        agent_column.append(agent1)
                        agent_column.append(agent2)

                        piece_column.append(column_name.values[i])
                        piece_column.append(column_name.values[i])

                    x_axis_label = [piece_column, agent_column]

                    # Create the figure and get the matches results
                    fig = go.Figure()
                    match_one_results = sacrifice_list[matches[0]]  # Agent 1 VS Agent 2, Red piece player
                    match_two_results = sacrifice_list[matches[1]]  # Agent 2 VS Agent 1, Black piece player
                    trace = 0

                    # Loop through all 5 games for the first match
                    for column in range(0, 30, 6):
                        # Create the empty dead pieces dataframe
                        revenge_piece_df = pd.DataFrame(revenge_piece, columns=['chess_piece', 'agent1', 'agent2'])

                        # Loop through the result of the games
                        for i in range(len(match_one_results[match_one_results.columns[column]])):
                            piece1 = match_one_results[match_one_results.columns[column + 2]].iloc[i]
                            piece2 = match_one_results[match_one_results.columns[column + 5]].iloc[i]

                            revenge_piece_df.loc[revenge_piece_df['chess_piece'] == piece1, ['agent1']] = \
                                revenge_piece_df.loc[revenge_piece_df['chess_piece'] == piece1]['agent1'] + 1

                            revenge_piece_df.loc[revenge_piece_df['chess_piece'] == piece2, ['agent2']] = \
                                revenge_piece_df.loc[revenge_piece_df['chess_piece'] == piece2]['agent2'] + 1

                        agent_one_revenged = list(revenge_piece_df[revenge_piece_df.columns[1]])
                        agent_two_revenged = list(revenge_piece_df[revenge_piece_df.columns[2]])

                        final_result = []

                        # Append the results into a final list to add to figure
                        for j in range(len(agent_one_revenged)):
                            final_result.append(agent_one_revenged[j])
                            final_result.append(agent_two_revenged[j])

                        fig.add_bar(x=x_axis_label, y=final_result, name=trace_name[trace] + ', Red Piece, Agent 1')
                        trace += 1

                    # Loop another 5 games for the second match
                    for column in range(0, 30, 6):
                        # Create the empty dead pieces dataframe
                        revenge_piece_df = pd.DataFrame(revenge_piece, columns=['chess_piece', 'agent1', 'agent2'])

                        # Loop through the result of the games
                        for i in range(len(match_two_results[match_two_results.columns[column]])):
                            piece1 = match_two_results[match_two_results.columns[column + 5]].iloc[i]
                            piece2 = match_two_results[match_two_results.columns[column + 2]].iloc[i]

                            revenge_piece_df.loc[revenge_piece_df['chess_piece'] == piece1, ['agent1']] = \
                                revenge_piece_df.loc[revenge_piece_df['chess_piece'] == piece1]['agent1'] + 1

                            revenge_piece_df.loc[revenge_piece_df['chess_piece'] == piece2, ['agent2']] = \
                                revenge_piece_df.loc[revenge_piece_df['chess_piece'] == piece2]['agent2'] + 1

                        agent_one_revenged = list(revenge_piece_df[revenge_piece_df.columns[1]])
                        agent_two_revenged = list(revenge_piece_df[revenge_piece_df.columns[2]])

                        final_result = []

                        # Append the results into a final list to add to figure
                        for j in range(len(agent_one_revenged)):
                            final_result.append(agent_one_revenged[j])
                            final_result.append(agent_two_revenged[j])

                        fig.add_bar(x=x_axis_label, y=final_result, name=trace_name[trace] + ', Black Piece, Agent 1')
                        trace += 1

                    fig.update_layout(barmode="relative", xaxis_title="Chess Piece",
                                      yaxis_title="Number of Chess Piece Revenged",
                                      title="Number of Chess Piece Revenged after Sacrificing a Chess Piece for " + agent1 +
                                            " VS " + agent2)
                    fig.show()

    # Visualising the Win percentage
    def win_rate_visualisation(self, outcome_list):
        result_dataframe = pd.DataFrame(columns=['agent1', 'agent2', 'Result'])
        game_number = 0
        for agent1 in self.agents_list:
            for agent2 in self.agents_list:
                agent1_outcome = 0.0

                if agent1 == agent2:
                    result_dataframe.loc[len(result_dataframe)] = [agent1, agent2, np.nan]
                else:
                    game_outcome = outcome_list[game_number]
                    game_number += 1
                    for row in range(len(game_outcome)):
                        if game_outcome.iloc[row][0] == 'Lose':
                            pass
                        elif game_outcome.iloc[row][0] == 'Win':
                            agent1_outcome += 1.0
                        else:
                            agent1_outcome += 0.5

                    result_dataframe.loc[len(result_dataframe)] = [agent1, agent2, str(agent1_outcome / 5 * 100)]

        result = pd.pivot_table(result_dataframe, index='agent1', columns='agent2', values='Result')

        fig, ax = plt.subplots(figsize=(13, 7))
        fig.canvas.manager.set_window_title('Agent Matches Win Percentage')
        sns.heatmap(result, annot=True, ax=ax, cmap='crest', fmt="")

        plt.title('Win Percentage (%) when Playing As Red Piece, Agent 1', fontsize=15)
        plt.xlabel('Black Piece, Agent 2', fontsize=15)
        plt.ylabel('Red Piece, Agent 1', fontsize=15)
        plt.show()

    # Visualising the total time taken
    def total_time_taken_visualisation(self, time_taken_list, matches_order):
        agent_shown = []
        time_column = []
        game_column = []
        matches = []
        y_value = []

        # Loop through the agents
        for agent1 in self.agents_list:
            for agent2 in self.agents_list:
                if agent1 == agent2:
                    pass
                else:
                    # Merge the agents together if they are versing the same agents, just might be playing as red or black piece
                    if [agent1, agent2] and [agent2, agent1] not in agent_shown:
                        matches.append(matches_order.index([agent1, agent2]))
                        agent_shown.append([agent1, agent2])
                        matches.append(matches_order.index([agent2, agent1]))
                        agent_shown.append([agent2, agent1])

                    else:
                        continue
        # Create the figure
        fig = go.Figure()

        # Create the X Axis Label
        for i in range(len(agent_shown)):
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            time_column.extend(
                [agent_shown[i][0] + ' Fastest', agent_shown[i][0] + ' Average', agent_shown[i][0] + ' Slowest',
                 agent_shown[i][1] + ' Fastest', agent_shown[i][1] + ' Average', agent_shown[i][1] + ' Slowest'])

        x_axis_label = [game_column, time_column]

        # Loop through the matches
        for i in range(len(agent_shown)):
            match = time_taken_list[matches[i]]

            agent1_highest = []
            agent2_highest = []
            agent1_lowest = []
            agent2_lowest = []
            agent1_average = []
            agent2_average = []

            # Loop through the games
            for column in range(0, 10, 2):
                agent1_match = match[match.columns[column]].dropna()
                agent2_match = match[match.columns[column + 1]].dropna()

                agent1_highest.append(max(agent1_match))
                agent2_highest.append(max(agent2_match))
                agent1_lowest.append(min(agent1_match))
                agent2_lowest.append(min(agent2_match))
                agent1_average.extend(list(agent1_match.values))
                agent2_average.extend(list(agent2_match.values))

            # Get the Y Values
            y_value.extend([min(agent1_lowest), sum(agent1_average) / len(agent1_average), max(agent1_highest),
                            min(agent2_lowest), sum(agent2_average) / len(agent2_average), max(agent2_highest)])

        # Create the Bar Figure
        fig.add_bar(x=x_axis_label, y=y_value)
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(xaxis=dict(tickfont=dict(size=10)), xaxis_title="Matches", yaxis_title="Time Taken (sec)",
                          title="Time Taken Experiments for the Agents")
        fig.show()

    # Visualising the total time taken
    def total_reward_visualisation(self, reward_list, matches_order):
        agent_shown = []
        reward_column = []
        game_column = []
        matches = []
        y_value = []

        # Loop through the agents
        for agent1 in self.agents_list:
            for agent2 in self.agents_list:
                if agent1 == agent2:
                    pass
                else:
                    # Merge the agents together if they are versing the same agents, just might be playing as red or black piece
                    if [agent1, agent2] and [agent2, agent1] not in agent_shown:
                        matches.append(matches_order.index([agent1, agent2]))
                        agent_shown.append([agent1, agent2])
                        matches.append(matches_order.index([agent2, agent1]))
                        agent_shown.append([agent2, agent1])

                    else:
                        continue
        # Create the figure
        fig = go.Figure()

        # Create the X Axis Label
        for i in range(len(agent_shown)):
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            game_column.extend([agent_shown[i][0] + '<br>VS<br>' + agent_shown[i][1]])
            reward_column.extend([agent_shown[i][0] + ' Lowest', agent_shown[i][0] + ' Average', agent_shown[i][0] + ' Highest',
                                  agent_shown[i][1] + ' Lowest', agent_shown[i][1] + ' Average', agent_shown[i][1] + ' Highest'])

        x_axis_label = [game_column, reward_column]
        print(x_axis_label)

        # Loop through the matches
        for i in range(len(agent_shown)):
            match = reward_list[matches[i]]

            agent1_total = []
            agent2_total = []

            # Loop through the games
            for column in range(0, 10, 2):
                agent1_match = match[match.columns[column]].dropna()
                agent2_match = match[match.columns[column + 1]].dropna()

                agent1_total.append(sum(agent1_match))
                agent2_total.append(sum(agent2_match))

            # Get the Y Values
            y_value.extend([min(agent1_total), sum(agent1_total) / len(agent1_total), max(agent1_total),
                            min(agent2_total), sum(agent2_total) / len(agent2_total), max(agent2_total)])

            print(y_value)

        # Create the Bar Figure
        fig.add_bar(x=x_axis_label, y=y_value)
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(xaxis=dict(tickfont=dict(size=10)), xaxis_title="Matches", yaxis_title="Reward Values",
                          title="Move Reward Experiments for the Agents")
        fig.show()

    # Visualising the Time Taken for each moves
    def time_taken_visualisation(self, time_taken_list, matches_order, trace_name):
        agent_shown = []

        # Loop through the agents
        for agent1 in self.agents_list:
            for agent2 in self.agents_list:
                matches = []
                if agent1 == agent2:
                    pass
                else:
                    # Merge the agents together if they are versing the same agents, just might be playing as red or black piece
                    if [agent1, agent2] and [agent2, agent1] not in agent_shown:
                        matches.append(matches_order.index([agent1, agent2]))
                        agent_shown.append([agent1, agent2])
                        matches.append(matches_order.index([agent2, agent1]))
                        agent_shown.append([agent2, agent1])
                    else:
                        continue

                    # Get the matches between the agents
                    match_1 = time_taken_list[matches[0]]  # Agent 1 VS Agent 2, Red piece player
                    match_2 = time_taken_list[matches[1]]  # Agent 1 VS Agent 2, Black piece player

                    fig = go.Figure()
                    trace = 0

                    # Loop through all 5 games for the first match
                    for game in range(0, len(match_1.columns), 2):
                        agent_1_game = match_1[match_1.columns[game]].dropna()

                        x = list(range(len(agent_1_game)))
                        fig.add_trace(go.Scatter(x=x, y=agent_1_game.values, name=agent1 + ', ' + trace_name[trace] + ', Red Piece',
                                                 line_shape='linear'))

                        agent_2_game = match_1[match_1.columns[game + 1]].dropna()
                        x = list(range(len(agent_2_game)))
                        fig.add_trace(go.Scatter(x=x, y=agent_2_game.values, name=agent2 + ', ' + trace_name[trace] + ', Black Piece',
                                                 line_shape='linear'))
                        trace += 1

                    # Loop through another 5 games for the second match
                    for game in range(0, len(match_2.columns), 2):
                        agent_1_game = match_2[match_2.columns[game + 1]].dropna()

                        x = list(range(len(agent_1_game)))
                        fig.add_trace(go.Scatter(x=x, y=agent_1_game.values, name=agent1 + ', ' + trace_name[trace] + ', Black Piece',
                                                 line_shape='linear'))

                        agent_2_game = match_2[match_2.columns[game]].dropna()
                        x = list(range(len(agent_2_game)))
                        fig.add_trace(go.Scatter(x=x, y=agent_2_game.values, name=agent2 + ', ' + trace_name[trace] + ', Red Piece',
                                                 line_shape='linear'))
                        trace += 1

                    fig.update_layout(barmode="relative", xaxis_title="Moves #", yaxis_title="Time Taken (sec)",
                                      title="Each Moves Time Taken for " + agent1 + " VS " + agent2)
                    fig.update_xaxes(rangeslider_visible=True, range=[0, 50])
                    fig.show()

    # Visualising the reward for each moves
    def reward_visualisation(self, reward_list, matches_order, trace_name):
        agent_shown = []

        # Loop through the agents
        for agent1 in self.agents_list:
            for agent2 in self.agents_list:
                matches = []
                if agent1 == agent2:
                    pass
                else:
                    # Merge the agents together if they are versing the same agents, just might be playing as red or black piece
                    if [agent1, agent2] and [agent2, agent1] not in agent_shown:
                        matches.append(matches_order.index([agent1, agent2]))
                        agent_shown.append([agent1, agent2])
                        matches.append(matches_order.index([agent2, agent1]))
                        agent_shown.append([agent2, agent1])
                    else:
                        continue

                    # Get the matches between the agents
                    match_1 = reward_list[matches[0]]  # Agent 1 VS Agent 2, Red piece player
                    match_2 = reward_list[matches[1]]  # Agent 1 VS Agent 2, Black piece player

                    fig = go.Figure()
                    trace = 0

                    # Loop through all 5 games for the first match
                    for game in range(0, len(match_1.columns), 2):
                        agent_1_game = match_1[match_1.columns[game]].dropna()

                        x = list(range(len(agent_1_game)))
                        fig.add_trace(go.Scatter(x=x, y=agent_1_game.values, name=agent1 + ', ' + trace_name[trace] + ', Red Piece',
                                                 line_shape='linear'))

                        agent_2_game = match_1[match_1.columns[game + 1]].dropna()
                        x = list(range(len(agent_2_game)))
                        fig.add_trace(go.Scatter(x=x, y=agent_2_game.values, name=agent2 + ', ' + trace_name[trace] + ', Black Piece',
                                                 line_shape='linear'))
                        trace += 1

                    # Loop through another 5 games for the second match
                    for game in range(0, len(match_2.columns), 2):
                        agent_1_game = match_2[match_2.columns[game + 1]].dropna()

                        x = list(range(len(agent_1_game)))
                        fig.add_trace(go.Scatter(x=x, y=agent_1_game.values, name=agent1 + ', ' + trace_name[trace] + ', Black Piece',
                                                 line_shape='linear'))

                        agent_2_game = match_2[match_2.columns[game]].dropna()
                        x = list(range(len(agent_2_game)))
                        fig.add_trace(go.Scatter(x=x, y=agent_2_game.values, name=agent2 + ', ' + trace_name[trace] + ', Red Piece',
                                                 line_shape='linear'))
                        trace += 1

                    fig.update_layout(barmode="relative", xaxis_title="Moves #", yaxis_title="Reward Values",
                                      title="Each Moves' Reward for " + agent1 + " VS " + agent2)
                    fig.update_yaxes(range=[-12, 12])
                    fig.update_xaxes(rangeslider_visible=True, range=[0, 50])
                    fig.show()

    def dead_pieces_visualisation(self, dead_list, matches_order, trace_name):
        agent_shown = []
        dead_piece = []
        # Put the list of dead pieces into list
        for i in range(1, len(PIECE_ID_TO_NAME)):
            dead_piece.append([PIECE_ID_TO_NAME[i], 0, 0])

        # Create the empty dead pieces dataframe
        dead_piece_df = pd.DataFrame(dead_piece, columns=['chess_piece', 'agent1', 'agent2'])

        # Loop through the agents
        for agent1 in self.agents_list:
            for agent2 in self.agents_list:
                matches = []
                if agent1 == agent2:
                    pass
                else:
                    # Merge the agents together if they are versing the same agents, just might be playing as red or black piece
                    if [agent1, agent2] and [agent2, agent1] not in agent_shown:
                        matches.append(matches_order.index([agent1, agent2]))
                        agent_shown.append([agent1, agent2])
                        matches.append(matches_order.index([agent2, agent1]))
                        agent_shown.append([agent2, agent1])
                    else:
                        continue

                    # Initialise the variables
                    column_name = dead_piece_df['chess_piece']
                    agent_column = []
                    piece_column = []

                    # Get the X axis label for the graph
                    for i in range(len(column_name.values)):
                        agent_column.append(agent1)
                        agent_column.append(agent2)

                        piece_column.append(column_name.values[i])
                        piece_column.append(column_name.values[i])

                    x_axis_label = [piece_column, agent_column]

                    # Create the figure and get the matches results
                    fig = go.Figure()
                    match_one_results = dead_list[matches[0]]  # Agent 1 VS Agent 2, Red piece player
                    match_two_results = dead_list[matches[1]]  # Agent 2 VS Agent 1, Black piece player
                    trace = 0

                    # Loop through all 5 games for the first match
                    for column in range(0, 10, 2):
                        # Create the empty dead pieces dataframe
                        dead_piece_df = pd.DataFrame(dead_piece, columns=['chess_piece', 'agent1', 'agent2'])

                        # Loop through the result of the games
                        for i in range(len(match_one_results[match_one_results.columns[column]])):
                            piece1 = match_one_results[match_one_results.columns[column]].iloc[i]
                            piece2 = match_one_results[match_one_results.columns[column + 1]].iloc[i]

                            dead_piece_df.loc[dead_piece_df['chess_piece'] == piece1, ['agent1']] = \
                                dead_piece_df.loc[dead_piece_df['chess_piece'] == piece1]['agent1'] + 1

                            dead_piece_df.loc[dead_piece_df['chess_piece'] == piece2, ['agent2']] = \
                                dead_piece_df.loc[dead_piece_df['chess_piece'] == piece2]['agent2'] + 1

                        agent_one_dead = list(dead_piece_df[dead_piece_df.columns[1]])
                        agent_two_dead = list(dead_piece_df[dead_piece_df.columns[2]])

                        final_result = []

                        # Append the results into a final list to add to figure
                        for j in range(len(agent_one_dead)):
                            final_result.append(agent_one_dead[j])
                            final_result.append(agent_two_dead[j])

                        fig.add_bar(x=x_axis_label, y=final_result, name=trace_name[trace] + ', Red Piece, Agent 1')
                        trace += 1

                    # Loop another 5 games for the second match
                    for column in range(0, 10, 2):
                        # Create the empty dead pieces dataframe
                        dead_piece_df = pd.DataFrame(dead_piece, columns=['chess_piece', 'agent1', 'agent2'])

                        # Loop through the result of the games
                        for i in range(len(match_two_results[match_two_results.columns[column]])):
                            piece1 = match_two_results[match_two_results.columns[column + 1]].iloc[i]
                            piece2 = match_two_results[match_two_results.columns[column]].iloc[i]

                            dead_piece_df.loc[dead_piece_df['chess_piece'] == piece1, ['agent1']] = \
                                dead_piece_df.loc[dead_piece_df['chess_piece'] == piece1]['agent1'] + 1

                            dead_piece_df.loc[dead_piece_df['chess_piece'] == piece2, ['agent2']] = \
                                dead_piece_df.loc[dead_piece_df['chess_piece'] == piece2]['agent2'] + 1

                        agent_one_dead = list(dead_piece_df[dead_piece_df.columns[1]])
                        agent_two_dead = list(dead_piece_df[dead_piece_df.columns[2]])

                        final_result = []

                        # Append the results into a final list to add to figure
                        for j in range(len(agent_one_dead)):
                            final_result.append(agent_one_dead[j])
                            final_result.append(agent_two_dead[j])

                        fig.add_bar(x=x_axis_label, y=final_result, name=trace_name[trace] + ', Black Piece, Agent 1')
                        trace += 1

                    fig.update_layout(barmode="relative", xaxis_title="Chess Piece", yaxis_title="Number of Death",
                                      title="Number of Chess Piece Death for " + agent1 + " VS " + agent2)
                    fig.show()

    # Visualising the total Chess Piece Movement
    def total_dead_piece_visualisation(self, dead_list, matches_order, agent_list):
        dead_piece = []
        # Put the list of dead pieces into list
        for i in range(1, len(PIECE_ID_TO_NAME)):
            dead_piece.append([PIECE_ID_TO_NAME[i], 0, 0])

        # Create the empty dead pieces dataframe
        dead_piece_df = pd.DataFrame(dead_piece, columns=['chess_piece', 'agent1', 'agent2'])

        column_name = dead_piece_df['chess_piece']
        agent_column = []
        piece_column = []
        for i in range(len(column_name.values)):
            agent_column.extend(agent_list)

            piece_column.append(column_name.values[i])
            piece_column.append(column_name.values[i])
            piece_column.append(column_name.values[i])
            piece_column.append(column_name.values[i])

        x_axis_label = [piece_column, agent_column]
        fig = go.Figure()

        for number, matches in enumerate(dead_list):
            added_agent_one = []
            added_agent_two = []

            for games in range(0, 10, 2):
                # Reset the dataframe
                dead_piece_df = pd.DataFrame(dead_piece, columns=['chess_piece', 'agent1', 'agent2'])

                # Loop through the result of the games
                for i in range(len(matches)):
                    piece1 = matches[matches.columns[games]].iloc[i]
                    piece2 = matches[matches.columns[games + 1]].iloc[i]

                    dead_piece_df.loc[dead_piece_df['chess_piece'] == piece1, ['agent1']] = \
                        dead_piece_df.loc[dead_piece_df['chess_piece'] == piece1]['agent1'] + 1

                    dead_piece_df.loc[dead_piece_df['chess_piece'] == piece2, ['agent2']] = \
                        dead_piece_df.loc[dead_piece_df['chess_piece'] == piece2]['agent2'] + 1

                agent_one = list(dead_piece_df[dead_piece_df.columns[1]])
                agent_two = list(dead_piece_df[dead_piece_df.columns[2]])

                if len(added_agent_one) == 0:
                    added_agent_one = agent_one
                    added_agent_two = agent_two
                else:
                    added_agent_one = [added_agent_one[i] + agent_one[i] for i in range(len(agent_one))]
                    added_agent_two = [added_agent_two[i] + agent_two[i] for i in range(len(agent_two))]

            final_result = []

            for j in range(len(added_agent_one)):
                if matches_order[number][0] == agent_list[0]:
                    final_result.append(added_agent_one[j])
                elif matches_order[number][1] == agent_list[0]:
                    final_result.append(added_agent_two[j])
                else:
                    final_result.append(0)

                if matches_order[number][0] == agent_list[1]:
                    final_result.append(added_agent_one[j])
                elif matches_order[number][1] == agent_list[1]:
                    final_result.append(added_agent_two[j])
                else:
                    final_result.append(0)

                if matches_order[number][0] == agent_list[2]:
                    final_result.append(added_agent_one[j])
                elif matches_order[number][1] == agent_list[2]:
                    final_result.append(added_agent_two[j])
                else:
                    final_result.append(0)

                if matches_order[number][0] == agent_list[3]:
                    final_result.append(added_agent_one[j])
                elif matches_order[number][1] == agent_list[3]:
                    final_result.append(added_agent_two[j])
                else:
                    final_result.append(0)

            fig.add_bar(x=x_axis_label, y=final_result,
                        name=matches_order[number][0] + " VS " + matches_order[number][1])

        fig.update_layout(barmode="relative", xaxis_title="Chess Piece", yaxis_title="Number of Death",
                          title="Total Number of Chess Piece Death for the Agents")
        fig.show()

    # Visualising the Chess Piece Movement per match
    def movement_visualisation(self, piece_list, matches_order, trace_name):
        agent_shown = []

        for agent1 in self.agents_list:
            for agent2 in self.agents_list:
                matches = []
                if agent1 == agent2:
                    pass
                else:
                    # Merge the agents together if they are versing the same agents, just might be playing as red or black piece
                    if [agent1, agent2] and [agent2, agent1] not in agent_shown:
                        matches.append(matches_order.index([agent1, agent2]))
                        agent_shown.append([agent1, agent2])
                        matches.append(matches_order.index([agent2, agent1]))
                        agent_shown.append([agent2, agent1])
                    else:
                        continue

                    # Initialise the variables
                    column_name = piece_list[matches[0]].iloc[1:]['chess_piece']
                    agent_column = []
                    piece_column = []

                    # Get the X axis label for the graph
                    for i in range(len(column_name.values)):
                        agent_column.append(agent1)
                        agent_column.append(agent2)

                        piece_column.append(column_name.values[i])
                        piece_column.append(column_name.values[i])

                    x_axis_label = [piece_column, agent_column]

                    # Create the figure and get the matches results
                    fig = go.Figure()
                    match_one_results = piece_list[matches[0]].iloc[1:]  # Agent 1 VS Agent 2, Red piece player
                    match_two_results = piece_list[matches[1]].iloc[1:]  # Agent 2 VS Agent 1, Black piece player
                    trace = 0

                    # Loop through all 5 games for the first match
                    for i in range(0, 10, 2):
                        result_one = list(match_one_results[match_one_results.columns[i + 1]])
                        result_two = list(match_one_results[match_one_results.columns[i + 2]])

                        final_result = []

                        # Append the results into a final list to add to figure
                        for j in range(len(result_one)):
                            final_result.append(result_one[j])
                            final_result.append(result_two[j])

                        fig.add_bar(x=x_axis_label, y=final_result, name=trace_name[trace] + ', Red Piece, Agent 1')
                        trace += 1

                    # Loop another 5 games for the second match
                    for i in range(0, 10, 2):
                        result_one = list(match_two_results[match_two_results.columns[i + 2]])
                        result_two = list(match_two_results[match_two_results.columns[i + 1]])

                        final_result = []

                        # Append the results into a final list to add to figure
                        for j in range(len(result_one)):
                            final_result.append(result_one[j])
                            final_result.append(result_two[j])

                        fig.add_bar(x=x_axis_label, y=final_result, name=trace_name[trace] + ', Black Piece, Agent 1')
                        trace += 1

                    fig.update_layout(barmode="relative", xaxis_title="Chess Piece", yaxis_title="Number of Moves",
                                      title="Number of Moves for " + agent1 + " VS " + agent2)
                    fig.show()

    # Visualising the total Chess Piece Movement
    def total_movement_visualisation(self, piece_list, matches_order, agent_list):
        column_name = piece_list[0].iloc[1:]['chess_piece']
        agent_column = []
        piece_column = []

        # Get the X axis label for the graph
        for i in range(len(column_name.values)):
            agent_column.extend(agent_list)

            piece_column.append(column_name.values[i])
            piece_column.append(column_name.values[i])
            piece_column.append(column_name.values[i])
            piece_column.append(column_name.values[i])

        x_axis_label = [piece_column, agent_column]

        fig = go.Figure()

        # Loop through the matches between the agents
        for number, matches in enumerate(piece_list):
            added_agent_one = []
            added_agent_two = []

            # loop through all 5 games from the matches
            for games in range(0, 10, 2):
                agent_one = list(matches[matches.columns[games + 1]].iloc[1:])
                agent_two = list(matches[matches.columns[games + 2]].iloc[1:])

                if len(added_agent_one) == 0:
                    added_agent_one = agent_one
                    added_agent_two = agent_two
                else:
                    added_agent_one = [added_agent_one[i] + agent_one[i] for i in range(len(agent_one))]
                    added_agent_two = [added_agent_two[i] + agent_two[i] for i in range(len(agent_two))]

            final_result = []

            # Put the result in the correct order
            for j in range(len(added_agent_one)):
                if matches_order[number][0] == agent_list[0]:
                    final_result.append(added_agent_one[j])
                elif matches_order[number][1] == agent_list[0]:
                    final_result.append(added_agent_two[j])
                else:
                    final_result.append(0)

                if matches_order[number][0] == agent_list[1]:
                    final_result.append(added_agent_one[j])
                elif matches_order[number][1] == agent_list[1]:
                    final_result.append(added_agent_two[j])
                else:
                    final_result.append(0)

                if matches_order[number][0] == agent_list[2]:
                    final_result.append(added_agent_one[j])
                elif matches_order[number][1] == agent_list[2]:
                    final_result.append(added_agent_two[j])
                else:
                    final_result.append(0)

                if matches_order[number][0] == agent_list[3]:
                    final_result.append(added_agent_one[j])
                elif matches_order[number][1] == agent_list[3]:
                    final_result.append(added_agent_two[j])
                else:
                    final_result.append(0)

            # Create the Bar
            fig.add_bar(x=x_axis_label, y=final_result,
                        name=matches_order[number][0] + " VS " + matches_order[number][1])

        fig.update_layout(barmode="relative", xaxis_title="Chess Piece", yaxis_title="Number of Moves",
                          title="Total Number of Moves for the Agents")
        fig.show()
