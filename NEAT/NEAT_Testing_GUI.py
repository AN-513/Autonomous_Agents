import random
import pickle
import neat
import os
from Envoirments import env_lighthouse
from Classes import agent, stats

best_agent = None

# Load the best agent.
with open('best_agent.pkl', 'rb') as f:
    best_agent = pickle.load(f)


env = env_lighthouse.Light_House(agent=best_agent, stats=None, light_reach=3, dimensions=(15, 15), num_walls=30, max_steps=200, random_seed=random.randint(0, 9999999))
env.display_gui()