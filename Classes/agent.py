import time
import random

class RandomAgent:
    def __init__(self):
        pass

    def make_decision(self, options:list, observations):
        return random.choice(options)


class NEAT_Agent:
    def __init__(self, genome, config):
        from neat.nn import FeedForwardNetwork
        self.genome = genome
        self.config = config
        self.net = FeedForwardNetwork.create(genome,config)

    def make_decision(self, options: list, observations: tuple):
        response = self.net.activate(observations["direcao_farol"])
        while len(response) > 0:
            best_option = response.index(max(response))
            if best_option in observations["invalid_options"]:
                response.pop(best_option)
            else:
                break
        if len(response) == 0:
            print("ERROR (agent.py): NO VALID MOVE FOUND")
        return options[best_option]


class Agent:
    def __init__(self, pure_agent):
        self.pure_agent = pure_agent

    def make_decision(self, options:list, observations:dict):
        return self.pure_agent.make_decision(options, observations)

