import random
import pickle
import neat
import os

from Classes.agent import Agent
from Envoirments import envoirment
from Classes import agent, stats, sensor

def get_direction_sensor(reference_name):
    _ds = sensor.DirectionSensor(reference_name)
    return [sensor.Sensor(_ds)]


bulk_stats = stats.StatsCluster()

# Load the best agent.
with open('neat_2624.pkl', 'rb') as f:
    neat_agent = pickle.load(f)

greedy_raw = agent.GreedyAgent()
greedy_agent = agent.Agent(greedy_raw, get_direction_sensor("lighthouse_pos"), memory_size=0)

random_raw = agent.RandomAgent()
random_agent = agent.Agent(random_raw, [], 0)

_agent = neat_agent


for i in range(2200):
    if i%100 == 0:
        print("Tested:", i, "simulations")
    _stats = stats.Stats()
    dim = 25
    num_walls = 15*int(i/100)
    #num_walls = 0
    env = envoirment.Light_House_Maze(agent=_agent, stats=_stats, light_reach=0, dimensions=(dim, dim), num_walls=num_walls, max_steps=2 * dim + 2 * num_walls, random_seed=random.randint(0, 9999999))
    #env.display_gui()
    env.run()
    bulk_stats.add_stats(_stats)

bulk_stats.display_plots()
bulk_stats.plot_win_rate_by_map_size()
bulk_stats.plot_win_rate_by_num_walls()




