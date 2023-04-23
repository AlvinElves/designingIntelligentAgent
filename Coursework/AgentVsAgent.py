import time
import gym
import pandas as pd

import matplotlib.pyplot as plt

from gym_xiangqi.agents import RandomAgent
from gym_xiangqi.constants import ALLY, PIECE_ID_TO_NAME
from gym_xiangqi.utils import action_space_to_move

env = gym.make('gym_xiangqi:xiangqi-v0')
env.reset()

agent = RandomAgent()

done = False
chess_round = 0
chess_list = []

for i in range(len(PIECE_ID_TO_NAME)):
    chess_list.append([PIECE_ID_TO_NAME[i], 0, 0])

move_df = pd.DataFrame(chess_list, columns=['chess_piece', 'enemy_move', 'ally_move'])

reward_df = pd.DataFrame([['Ally', 0], ['Enemy', 0]], columns=['user', 'reward'])

while not done:
    # Add a slight delay to properly visualize the game.
    time.sleep(1)

    action = agent.move(env)
    print(action)
    print(type(action))
    obs, reward, done, _ = env.step(action)
    print(obs)
    """turn = "Ally" if env.turn == ALLY else "Enemy"
    move = action_space_to_move(action)

    piece = PIECE_ID_TO_NAME[move[0]]

    if turn == 'Ally':
        move_df.loc[move_df['chess_piece'] == piece, ['ally_move']] = \
            move_df.loc[move_df['chess_piece'] == piece]['ally_move'] + 1

    elif turn == 'Enemy':
        move_df.loc[move_df['chess_piece'] == piece, ['enemy_move']] = \
            move_df.loc[move_df['chess_piece'] == piece]['enemy_move'] + 1

    reward_df.loc[reward_df['user'] == turn, ['reward']] = reward_df.loc[reward_df['user'] == turn]['reward'] + reward

    print(f"Round: {chess_round}")
    print(f"{turn} made the move {piece} from {move[1]} to {move[2]}.")
    print(f"Reward: {reward}")
    print("================")"""

    chess_round += 1
    #env.render()
env.close()

print(reward_df)

# Remove the matplotlib toolbar
plt.rcParams['toolbar'] = 'None'

# Plot the Number of Move for each chess piece
move_df[1:].plot.bar(x='chess_piece', rot=0, subplots=True, figsize=(14, 8), fontsize=6, title=['', ''])
plt.xticks(rotation=90, ha="right", rotation_mode="anchor")

plt.show()
