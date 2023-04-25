from Agent1VsAgent2 import single_experiment


def multi_run_experiment(visualise, agent1, agent2):
    for run in range(5):
        print(f"Run Number: {run + 1}, {agent1} VS {agent2}")
        single_experiment(visualise, agent1, agent2)


def multi_agent_experiment(visualise):
    agents_list = ['random_agent', 'minimax_agent', 'alpha_beta_agent', 'monte_carlo_agent']
    for agent1 in agents_list:
        for agent2 in agents_list:
            if agent1 != agent2:
                multi_run_experiment(visualise, agent1, agent2)


if __name__ == '__main__':
    multi_agent_experiment(False)
