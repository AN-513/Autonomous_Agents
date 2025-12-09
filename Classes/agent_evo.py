import random


class EvoAgent:
    def __init__(self, dna_length=100):
        # Genoma: Lista de inteiros representando direções
        # 0: Cima, 1: Baixo, 2: Esq, 3: Dir
        self.dna = [random.randint(0, 3) for _ in range(dna_length)]
        self.current_step = 0

        # Behavior Characterization (x, y final)
        self.final_pos = (0, 0)

        self.steps_taken = 0

        # Pontuações
        self.novelty_score = 0.0
        self.fitness = 0.0  # Score combinado (Novelty + Objetivo)

    def get_action(self):
        if self.current_step < len(self.dna):
            move = self.dna[self.current_step]
            self.current_step += 1
            # Mapear inteiro para tuplo de direção
            mapping = {0: (0, -1), 1: (0, 1), 2: (-1, 0), 3: (1, 0)}
            return mapping[move]
        return (0, 0)

    def mutate(self, mutation_rate=0.05):
        # Pequena probabilidade de mudar cada gene (movimento)
        for i in range(len(self.dna)):
            if random.random() < mutation_rate:
                self.dna[i] = random.randint(0, 3)

    def crossover(self, partner):
        """
        Cria um filho combinando o DNA deste agente com um parceiro (Single Point Crossover).
        Técnica essencial para recombinação genética.
        """
        child = EvoAgent(dna_length=len(self.dna))

        # Ponto de corte aleatório
        midpoint = random.randint(0, len(self.dna))

        # Combina metade de um com metade do outro
        child.dna = self.dna[:midpoint] + partner.dna[midpoint:]
        return child

    def reset(self):
        self.current_step = 0