import random
import pickle
import time
import math
import neat
import os
import multiprocessing
from Envoirments import envoirment
from Classes import agent, stats, sensor


MEMORY_SIZE = 3
RECURSIVE_SIZE = 0

GLOBAL_BEST_FITNESS = None
GLOBAL_BEST_FILE = None
SAVE_LOCK = None

def load_best_from_disk():
    best_fitness = -1
    best_file = None

    for file in os.listdir():
        if file.startswith("neat_") and file.endswith(".pkl"):
            try:
                fitness = int(file.replace("neat_", "").replace(".pkl", ""))
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_file = file
            except ValueError:
                pass

    return best_fitness, best_file


def init_worker(shared_fitness, shared_file, lock):
    global GLOBAL_BEST_FITNESS, GLOBAL_BEST_FILE, SAVE_LOCK
    GLOBAL_BEST_FITNESS = shared_fitness
    GLOBAL_BEST_FILE = shared_file
    SAVE_LOCK = lock


def get_sensors():
    all_sensors = []
    direction_sensor = sensor.DirectionSensor("lighthouse_pos")
    all_sensors.append(sensor.Sensor(direction_sensor))
    wall_sensor = sensor.WallSensor(2)
    all_sensors.append(sensor.Sensor(wall_sensor))
    return all_sensors


def eval_function(genome, config):
    neat_agent = agent.NEAT_Agent(genome, config, RECURSIVE_SIZE)
    sensors = get_sensors()
    bot = agent.Agent(neat_agent, sensors, memory_size=MEMORY_SIZE)

    fitness_list = []
    best_fitness = -9999999999

    basic_fitness = 0
    fitness_with_novelty_search = 0

    counter_wins = 0
    n_walls = 0
    MAX_ATTEMPTS = 5
    ATTEMPTS = 0

    while ATTEMPTS < MAX_ATTEMPTS:
        ATTEMPTS += 1
        if best_fitness > 0:
            MAX_ATTEMPTS = max(MAX_ATTEMPTS, math.log2(best_fitness**2))

        while True:
            seed = random.random()
            size_map = 20
            max_steps = 2 * size_map + 2 * n_walls

            env = envoirment.Light_House_Maze(
                bot,
                None,
                light_reach=size_map,
                dimensions=(size_map, size_map),
                num_walls=n_walls,
                max_steps=max_steps,
                random_seed=seed
            )

            env_output = env.run()

            if env_output[1] == 0:
                fitness_with_novelty_search += 1 + 0.1*round(env_output[2]/env_output[0], 5)
                basic_fitness += 1
                counter_wins += 1
                n_walls = int(counter_wins / (2 * MAX_ATTEMPTS))
            else:
                fitness_list.append(fitness_with_novelty_search)    # todo: IMPORTANT
                best_fitness = max(fitness_list)
                break

    average_fitness = float(sum(fitness_list) / len(fitness_list))
    int_fitness = int(average_fitness)

    # ========= SAFE GLOBAL SAVE =========
    with SAVE_LOCK:
        if int_fitness > GLOBAL_BEST_FITNESS.value:
            GLOBAL_BEST_FITNESS.value = int_fitness

            old_file = GLOBAL_BEST_FILE.get("file")
            if old_file and os.path.exists(old_file):
                os.remove(old_file)

            filename = f"neat_{int_fitness}.pkl"
            GLOBAL_BEST_FILE["file"] = filename

            best_agent = agent.Agent(
                agent.NEAT_Agent(genome, config, RECURSIVE_SIZE),
                get_sensors(),
                memory_size=MEMORY_SIZE
            )

            with open(filename, "wb") as f:
                pickle.dump(best_agent, f)

            print(f"[NEW BEST EVER] Saved {filename}")
    # ===================================

    return average_fitness


if __name__ == "__main__":
    multiprocessing.freeze_support()

    MAX_GENERATIONS = 20000

    # ---- create shared state safely ----
    manager = multiprocessing.Manager()
    shared_fitness = manager.Value("i", -1)
    shared_file = manager.dict()
    save_lock = manager.Lock()

    # ---- load best from disk ----
    disk_best_fitness, disk_best_file = load_best_from_disk()
    shared_fitness.value = disk_best_fitness
    if disk_best_file:
        shared_file["file"] = disk_best_file

    # ---- NEAT setup ----
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    population = neat.Population(config)
    population.add_reporter(neat.StatisticsReporter())
    population.add_reporter(neat.StdOutReporter(True))

    # ---- ParallelEvaluator (Windows-safe) ----
    pe = neat.ParallelEvaluator(
        os.cpu_count(),
        eval_function,
        initializer=init_worker,
        initargs=(shared_fitness, shared_file, save_lock),
    )

    population.run(pe.evaluate, n=MAX_GENERATIONS)
