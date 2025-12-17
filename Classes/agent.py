import time
import random
import sys

class RandomAgent:
    def __init__(self):
        pass

    def make_decision(self, options:list, agent_input:tuple):
        return random.choice(options)


class NEAT_Agent:
    def __init__(self, genome, config):
        from neat.nn import FeedForwardNetwork
        self.genome = genome
        self.config = config
        self.net = FeedForwardNetwork.create(genome,config)

    def make_decision(self, options: list, agent_input:tuple):
        response = self.net.activate(agent_input)
        best_option = response.index(max(response))
        return options[best_option]


class Agent:
    def __init__(self, pure_agent, sensors:list, memory_size:int):
        self.pure_agent = pure_agent
        self.sensors = sensors
        self.decision_counter = 0
        self.decision_history = []
        self.memory_size = memory_size
        self.clear_memory()


    def clear_memory(self):
        self.decision_history = []
        for _ in range(self.memory_size):
            self.decision_history.append(0)


    def make_decision(self, options:list, observations:dict, invalid_options:list):
        agent_input_raw = []

        if self.memory_size > 0:
            for mem in self.decision_history:
                agent_input_raw.append(mem)

        for sensor in self.sensors:
            local_input = sensor.get_sensor_data(observations)
            for value in local_input:
                if type(value) == list:
                    print("WARNING (agent.py): Not extracting the sensor data correctly")   # security check
                    time.sleep(5)
                agent_input_raw.append(value)

        agent_input = tuple(agent_input_raw)
        decision = self.pure_agent.make_decision(options, agent_input)
        security_counter = 0

        while decision in invalid_options:
            decision = random.choice(options)
            security_counter += 1
            if security_counter % 1000 == 0:
                print("WARNING (agent.py): stuck in invalid options!")
                print("Number of decisions:", self.decision_counter)
                print("Decision history:", self.decision_history)
                print("options:", options)
                print("invalid options:", invalid_options)
                time.sleep(5)
                sys.exit(-1)

        self.decision_counter += 1
        self.decision_history.append(options.index(decision)/5)

        if len(self.decision_history) > self.memory_size:
            self.decision_history.pop(0)

        return decision

