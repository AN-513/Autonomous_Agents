import math
import random
from Classes import stats, agent_evo


class NoveltySearch:
    def __init__(self, pop_size=50, archive_threshold=2.0, k_neighbors=15, mutation_rate=0.1, max_steps=100):
        self.pop_size = pop_size
        self.archive_threshold = archive_threshold
        self.k_neighbors = k_neighbors
        self.mutation_rate = mutation_rate
        self.max_steps = max_steps

        # População inicial
        self.population = [EvoAgent(dna_length=max_steps) for _ in range(pop_size)]
        self.archive = []  # Lista de behaviors (tuplos x,y) passados

    def evaluate_population(self, width, height, num_walls):
        # 1. Simular cada agente (Modo Aprendizagem - Rápido, sem GUI)
        for agent in self.population:
            agent.reset()
            # Criar ambiente temporário para teste
            # Nota: É crucial que o mapa seja O MESMO para todos na mesma geração
            # Para simplificar, assumimos que geramos um mapa fixo no main e passamos aqui
            # mas como a tua classe Light_House gera no init, vamos adaptar.

            # ATENÇÃO: Precisas de modificar o Light_House para aceitar um mapa fixo ou seed
            # Aqui vou assumir uma função auxiliar que corre a simulação 'headless'
            final_pos = self.run_simulation_headless(agent, width, height, num_walls)
            agent.final_pos = final_pos

        # 2. Calcular Novidade
        for agent in self.population:
            agent.novelty_score = self.calculate_novelty(agent)

    def calculate_novelty(self, agent):
        # Compara comportamento do agente (pos final) com a população atual + arquivo
        all_behaviors = [a.final_pos for a in self.population if a != agent] + self.archive

        if not all_behaviors:
            return 0.0

        # Calcular distâncias euclidianas
        distances = []
        x1, y1 = agent.final_pos
        for (x2, y2) in all_behaviors:
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            distances.append(dist)

        # Encontrar os k vizinhos mais próximos [cite: 133]
        distances.sort()
        k_nearest = distances[:self.k_neighbors]

        if not k_nearest:
            return 0.0

        # Média das distâncias
        novelty = sum(k_nearest) / len(k_nearest)
        return novelty

    def run_simulation_headless(self, agent, w, h, walls):
        # Versão simplificada do teu Light_House.run() sem pygame
        # Cria ambiente (idealmente passavas a lista de paredes para ser igual sempre)
        dummy_stats = stats.Stats()

        # NOTA: Isto vai gerar um mapa novo a cada agente, o que é mau para evolução.
        # O ideal é gerar o mapa UMA VEZ fora e passar as paredes.
        # Vou assumir aqui uma lógica simplificada de movimento.

        px, py = w // 2, h - 2  # Posição inicial do teu código

        for _ in range(self.max_steps):
            dx, dy = agent.get_action()
            nx, ny = px + dx, py + dy

            # Verificações básicas (limites)
            # Para ser perfeito, terias de passar o dicionário de paredes aqui
            if 0 <= nx < w and 0 <= ny < h:
                px, py = nx, ny

        return (px, py)

    def evolve(self):
        # 1. Atualizar Arquivo
        # Se um agente for muito inovador, adiciona ao arquivo [cite: 141]
        for agent in self.population:
            if agent.novelty_score > self.archive_threshold:
                self.archive.append(agent.final_pos)

        # 2. Seleção (Torneio ou Truncation)
        # Ordenar por novidade (descendente)
        self.population.sort(key=lambda x: x.novelty_score, reverse=True)

        # Elitismo: Manter os top 10%
        num_elites = int(self.pop_size * 0.1)
        next_gen = self.population[:num_elites]

        # Reprodução
        while len(next_gen) < self.pop_size:
            parent = random.choice(self.population[:self.pop_size // 2])  # Escolher dos melhores 50%
            child = EvoAgent(dna_length=self.max_steps)
            child.dna = parent.dna[:]  # Copiar genes
            child.mutate(self.mutation_rate)  # Mutar
            next_gen.append(child)

        self.population = next_gen

    def get_best_agent(self):
        # Retorna o agente com maior novidade (ou podes alterar para retornar o que chegou mais perto)
        self.population.sort(key=lambda x: x.novelty_score, reverse=True)
        return self.population[0]