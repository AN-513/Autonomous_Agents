import random
import pickle
import neat
import os
from Envoirments import env_lighthouse
from Classes import agent, stats, sensor


MEMORY_SIZE = 10

def get_sensors():
    all_sensors = []
    direction_sensor = sensor.DirectionSensor("lighthouse_pos")
    all_sensors.append(sensor.Sensor(direction_sensor))
    wall_sensor = sensor.WallSensor(2)
    all_sensors.append(sensor.Sensor(wall_sensor))
    light_sensor = sensor.LightSensor()
    all_sensors.append(light_sensor)
    return all_sensors


def eval_function(genome, config):
    neat_agent = agent.NEAT_Agent(genome, config)
    sensors = get_sensors()
    bot = agent.Agent(neat_agent, sensors, memory_size=MEMORY_SIZE)
    statistics = stats.StatsCluster()
    fitness = 1000
    n_walls = 0
    for i in range(50):
        stat = stats.Stats()
        env = env_lighthouse.Light_House(bot, stat, 3, dimensions=(15, 15), num_walls=n_walls, max_steps=200, random_seed=random.randint(1, 99999999))
        env_output = env.run()
        statistics.add_stats(stat)
        fitness -= env_output[0]
        fitness -= env_output[1]
        fitness += 2 * env_output[2]
        fitness += 5 * n_walls
        if env_output[1] == 0:
            n_walls += 1
    return fitness

if __name__ == "__main__":
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

    best_genome = population.run(pe.evaluate)
    neat_agent = agent.NEAT_Agent(best_genome, config)
    best_agent = agent.Agent(neat_agent, get_sensors(), memory_size=MEMORY_SIZE)

    # Save the best agent.
    with open('best_agent.pkl', 'wb') as f:
        pickle.dump(best_agent, f)

