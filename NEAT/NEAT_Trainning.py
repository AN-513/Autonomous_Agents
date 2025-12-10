import random
import pickle
import neat
import os
from Envoirments import env_lighthouse
from Classes import agent, stats


def eval_function(genome, config):
    bot = agent.NEAT_Agent(genome, config)
    statistics = stats.StatsCluster()
    fitness = 100
    for i in range(1):
        stat = stats.Stats()
        env = env_lighthouse.Light_House(bot, stat, 0, 10, 10, 0, max_steps=100, random_seed=2)
        env_output = env.run()
        statistics.add_stats(stat)
        fitness -= env_output[0]
        fitness -= env_output[1]
    return fitness

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    population = neat.Population(config)

    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.StdOutReporter(True))
    filenamePrefix = r'C:\Users\Afonso Noia\PycharmProjects\Autonomous_Agents\NEAT\backups\\'
    population.add_reporter(neat.Checkpointer(filename_prefix=filenamePrefix, generation_interval=1))

    pe = neat.ParallelEvaluator(os.cpu_count(), eval_function)

    winner = population.run(pe.evaluate)

    # Save the winner.
    with open('winner', 'wb') as f:
        pickle.dump(winner, f)

