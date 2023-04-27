import pandas as pd

from Agent1VsAgent2 import single_experiment


def multi_run_experiment(visualise, agent1, agent2):
    time_taken_df = pd.DataFrame()
    for run in range(2):
        print(f"Run Number: {run + 1}, {agent1} VS {agent2}")
        list_of_result = single_experiment(visualise, agent1, agent2)
        run_number = 'run ' + str(run + 1)

        time_taken_df[agent1 + ' time taken ' + run_number] = list_of_result[0][0]
        time_taken_df[agent2 + ' time taken ' + run_number] = list_of_result[0][1]

        print(time_taken_df)


def multi_agent_experiment(visualise):
    agents_list = ['random_agent', 'minimax_agent', 'alpha_beta_agent', 'monte_carlo_agent']
    for agent1 in agents_list:
        for agent2 in agents_list:
            if agent1 != agent2:
                multi_run_experiment(visualise, agent1, agent2)


if __name__ == '__main__':
    multi_run_experiment(False, 'random_agent', 'alpha_beta_agent')
    #multi_agent_experiment(False)
