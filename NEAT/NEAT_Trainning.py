import random
import pickle
import time
import math
import neat
import os
from Envoirments import env_lighthouse
from Classes import agent, stats, sensor


MEMORY_SIZE = 10

def get_sensors():
    all_sensors = []
    direction_sensor = sensor.DirectionSensor("lighthouse_pos")
    all_sensors.append(sensor.Sensor(direction_sensor))
    #wall_sensor = sensor.WallSensor(2)
    #all_sensors.append(sensor.Sensor(wall_sensor))
    #light_sensor = sensor.LightSensor()
    #all_sensors.append(light_sensor)
    return all_sensors


def eval_function(genome, config):
    neat_agent = agent.NEAT_Agent(genome, config)
    sensors = get_sensors()
    bot = agent.Agent(neat_agent, sensors, memory_size=MEMORY_SIZE)
    statistics = stats.StatsCluster()

    fitness_list = []
    best_fitness = -9999999999

    main_random = 653186532 #int(time.time()/600)

    for i in range(5):
        fitness_positive = 1
        fitness_negative = 1
        one_win = True

        num_wins = 0
        MAX_WINS = 10000

        n_walls = 0
        size_map = 10
        light_range = 0
        max_steps = 25
        seed = main_random


        while one_win and num_wins < MAX_WINS:
            one_win = False
            stat = stats.Stats()
            if num_wins <= 100:
                n_walls = 0
                size_map = int(3 + (num_wins / 10))
                light_range = 0
                max_steps = 2*size_map + 10
                seed = main_random - 100*num_wins**2 + 500 * i
            else:
                n_walls = int((num_wins-100)/20)
                size_map = 15
                light_range = 0
                max_steps = 2 * size_map + 10
                seed = main_random - num_wins ** 2 + 500 * i

            env = env_lighthouse.Light_House(bot, stat, light_range, dimensions=(size_map, size_map), num_walls=n_walls, max_steps=max_steps, random_seed=seed)
            env_output = env.run() #.run()
            statistics.add_stats(stat)
            fitness_negative += env_output[0]
            fitness_negative += env_output[1] - env.get_i_distance()
            fitness_positive += env_output[2]

            if env_output[1] == 0:
                one_win = True
                num_wins += 1
                n_walls += 1
                fitness_positive += env.get_i_distance()
            else:
                n_walls = 0

        fitness_positive += n_walls ** 1.5
        fitness = num_wins #round(fitness_positive/fitness_negative, 2)
        fitness_list.append(fitness)
        best_fitness = max(best_fitness, fitness)

    average_fitness = float(sum(fitness_list) / len(fitness_list))
    return average_fitness

if __name__ == "__main__":

    MAX_GENERATIONS = 100

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    population = neat.Population(config)

    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.StdOutReporter(True))
    #filenamePrefix = r'C:\Users\Afonso Noia\PycharmProjects\Autonomous_Agents\NEAT\backups\\'
    #population.add_reporter(neat.Checkpointer(filename_prefix=filenamePrefix, generation_interval=1))

    pe = neat.ParallelEvaluator(os.cpu_count(), eval_function) # TODO:

    best_genome = population.run(pe.evaluate, n=MAX_GENERATIONS)
    neat_agent = agent.NEAT_Agent(best_genome, config)
    best_agent = agent.Agent(neat_agent, get_sensors(), memory_size=MEMORY_SIZE)

    # Save the best agent.
    with open('neat_2_2.pkl', 'wb') as f:
        pickle.dump(best_agent, f)

