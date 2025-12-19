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


class GreedyFixedAgent:
    def __init__(self, memory_size):
        self.memory_size = memory_size

    def make_decision(self, options: list, agent_input: tuple):
        # Como definido em NEAT_Trainning, o DirectionSensor vem após a memória.
        # Se MEMORY_SIZE = 10, dx está no índice 10 e dy no índice 11.
        dx = agent_input[self.memory_size]
        dy = agent_input[self.memory_size + 1]

        # Lógica fixa: priorizar o eixo onde a distância é maior
        if abs(dx) >= abs(dy):
            if dx > 0 and (1, 0) in options: return (1, 0)
            if dx < 0 and (-1, 0) in options: return (-1, 0)

        if dy > 0 and (0, 1) in options: return (0, 1)
        if dy < 0 and (0, -1) in options: return (0, -1)

        # Caso a direção ideal esteja bloqueada ou dx/dy sejam 0
        return random.choice(options)


class SmartGreedyFixedAgent:
    def __init__(self, memory_size):
        self.memory_size = memory_size

    def make_decision(self, options: list, agent_input: tuple):
        # 1. Extrair direção do farol (índices 10 e 11) [cite: 918, 926]
        dx_dir = agent_input[self.memory_size]
        dy_dir = agent_input[self.memory_size + 1]

        # 2. Mapear direções ideais baseadas na posição do farol
        ideal_moves = []
        if dx_dir > 0: ideal_moves.append((1, 0))
        elif dx_dir < 0: ideal_moves.append((-1, 0))
        if dy_dir > 0: ideal_moves.append((0, 1))
        elif dy_dir < 0: ideal_moves.append((0, -1))

        # 3. Filtrar apenas movimentos que estão nas 'options' (não bloqueados pelo ambiente)
        # O simulador já remove movimentos que saem do mapa ou batem em paredes [cite: 80, 114]
        valid_ideal_moves = [move for move in ideal_moves if move in options]

        if valid_ideal_moves:
            # Se houver mais do que um movimento ideal, escolhe o que tem menos obstáculos próximos
            # ou alterna entre eles para evitar o vício horizontal
            return random.choice(valid_ideal_moves)

        # 4. Se os movimentos ideais estiverem bloqueados, tenta um desvio (Norte/Sul/Este/Oeste)
        # Escolhe qualquer opção válida que não seja a direção oposta ao farol
        for alt_move in options:
            # Evita voltar para trás se possível
            if (dx_dir > 0 and alt_move == (-1, 0)) or (dy_dir > 0 and alt_move == (0, -1)):
                continue
            return alt_move

        return random.choice(options)

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

