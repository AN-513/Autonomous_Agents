import random
import pickle
import time
import math
import neat
import os
from Envoirments import env_lighthouse
from Classes import agent, stats, sensor


MEMORY_SIZE = 1

def get_sensors():
    all_sensors = []
    direction_sensor = sensor.DirectionSensor("lighthouse_pos")
    all_sensors.append(sensor.Sensor(direction_sensor))
    #laser_sensor = sensor.LaserSensor(3)
    #all_sensors.append(laser_sensor)
    wall_sensor = sensor.WallSensor(2)
    all_sensors.append(sensor.Sensor(wall_sensor))
    #light_sensor = sensor.LightSensor()
    #all_sensors.append(light_sensor)
    return all_sensors


def eval_function(genome, config):
    neat_agent = agent.NEAT_Agent(genome, config, 1)
    sensors = get_sensors()
    bot = agent.Agent(neat_agent, sensors, memory_size=MEMORY_SIZE)
    statistics = stats.StatsCluster()

    fitness_list = []
    best_fitness = -9999999999

    main_random = int(time.time()/600)

    basic_fitness = 0
    counter_wins = 0
    n_walls = 0
    ATTEMPTS = 10
    for i in range(ATTEMPTS):
        while True:
            seed = random.random()
            size_map = 20
            env = env_lighthouse.Light_House(bot, None, light_reach=size_map, dimensions=(size_map, size_map), num_walls=n_walls, max_steps=2*size_map+2*n_walls, random_seed=seed)
            env_output = env.run()
            #env_output = env.display_gui()
            if env_output[1] == 0:
                basic_fitness += 1
                counter_wins += 1
                n_walls = int(counter_wins/25)
            else:
                fitness_list.append(basic_fitness)
                break

    average_fitness = float(sum(fitness_list) / len(fitness_list))
    return average_fitness

if __name__ == "__main__":

    MAX_GENERATIONS = 500

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
    #pe = neat.ParallelEvaluator(1, eval_function)

    best_genome = population.run(pe.evaluate, n=MAX_GENERATIONS)
    neat_agent = agent.NEAT_Agent(best_genome, config)
    best_agent = agent.Agent(neat_agent, get_sensors(), memory_size=MEMORY_SIZE)

    # Save the best agent.
    with open('neat.pkl', 'wb') as f:
        pickle.dump(best_agent, f)

