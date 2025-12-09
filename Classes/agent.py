import time
import random

class RandomAgent:
    def __init__(self):
        pass

    def make_decision(self, options:list, observations):
        return random.choice(options)


class Agent:
    def __init__(self, pure_agent):
        self.pure_agent = pure_agent

    def make_decision(self, options:list, observations:dict):
        return self.pure_agent.make_decision(options, observations)

