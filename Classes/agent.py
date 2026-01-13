import time
import random
import sys

class RandomAgent:
    def __init__(self):
        pass

    def make_decision(self, options:list, agent_input:tuple):
        return random.choice(options)

class GreedyAgent:
    def __init__(self):
        pass

    def make_decision(self, options:list, agent_input:tuple):
        decision = list(agent_input)
        if decision[0] != 0:
            decision[1] = 0
        return decision


class NEAT_Agent:
    def __init__(self, genome, config, recursive_size:int):
        from neat.nn import FeedForwardNetwork
        self.genome = genome
        self.config = config
        self.net = FeedForwardNetwork.create(genome,config)
        self.recursive_size = recursive_size
        self.recursive_values = []
        for _ in range(recursive_size):
            self.recursive_values.append(0)

    def make_decision(self, options: list, agent_input_raw:tuple):
        #print(agent_input)
        agent_input = list(agent_input_raw)
        for val in self.recursive_values:
            agent_input.append(val)
        response = self.net.activate(agent_input)
        filtred_response = response[0:len(response)-self.recursive_size]
        for i in range(self.recursive_size):
            self.recursive_values.pop(0)
            self.recursive_values.append(response[-1-i])
        best_option = filtred_response.index(max(filtred_response))

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
            for __ in range(4):
                self.decision_history.append(0)

    def add_decision_to_memory(self, decision_index:int):
        mem = [0, 0, 0, 0]
        mem[decision_index] = 1
        for val in mem:
            self.decision_history.append(val)
        while len(self.decision_history) > len(mem)*self.memory_size:
            self.decision_history.pop(0)

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

        while decision in invalid_options:
            decision = random.choice(options)

        self.decision_counter += 1

        return decision

