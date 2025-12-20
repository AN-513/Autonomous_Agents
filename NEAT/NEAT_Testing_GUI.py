import random
import pickle
import neat
import os

from Classes.agent import Agent
from Envoirments import env_lighthouse
from Classes import agent, stats, sensor

def get_direction_sensor(reference_name):
    _ds = sensor.DirectionSensor(reference_name)
    return [sensor.Sensor(_ds)]


bulk_stats = stats.StatsCluster()

# Load the best agent.
with open('neat_2_2.pkl', 'rb') as f:
    neat_agent = pickle.load(f)

greedy_raw = agent.GreedyAgent()
greedy_agent = agent.Agent(greedy_raw, get_direction_sensor("lighthouse_pos"), memory_size=0)

random_raw = agent.RandomAgent()
random_agent = agent.Agent(random_raw, [], 0)

_agent = neat_agent

for i in range(1000):
    _stats = stats.Stats()
    dim = int(5 + i/100)
    num_walls = 5*int(i/50)
    #num_walls = 0
    env = env_lighthouse.Light_House(agent=_agent, stats=_stats, light_reach=0, dimensions=(dim,dim), num_walls=num_walls, max_steps=200, random_seed=random.randint(0, 9999999))
    env.run() #.display_gui()
    bulk_stats.add_stats(_stats)

bulk_stats.display_plots()
bulk_stats.plot_win_rate_by_map_size()
bulk_stats.plot_win_rate_by_num_walls()




