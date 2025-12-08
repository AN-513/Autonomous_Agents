import time
import random

# only random for now
class Agent:
    def __init__(self):
        time.sleep(1)

    def make_decision(self, options:list):
        return random.choice(options)

