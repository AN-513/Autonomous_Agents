import math
import random
from Classes import agent_evo, stats, items
from Envoirments import env_lighthouse

# --- CONFIGURAÇÕES DO TREINO ---
POP_SIZE = 100  # População maior ajuda a explorar mais caminhos [cite: 145]
GENERATIONS = 100  # Mais gerações para permitir otimização de passos
K_NEIGHBORS = 15  # Vizinhos para cálculo de novidade [cite: 133]
ARCHIVE_THRESHOLD = 6.0  # Limiar para adicionar ao arquivo [cite: 141]
DNA_LENGTH = 200  # Tamanho máximo do caminho
MAP_W, MAP_H = 20, 20  # Dimensões
NUM_WALLS = 90  # Complexidade do mapa


def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def main():
    # 1. SETUP DO AMBIENTE (Mapa Fixo)
    # Gerar paredes uma única vez para garantir justiça na avaliação
    dummy_agent = agent_evo.EvoAgent()
    dummy_stats = stats.Stats()
    base_env = env_lighthouse.Light_House(dummy_agent, dummy_stats, width=MAP_W, height=MAP_H, num_walls=NUM_WALLS)
    fixed_items = base_env.itemsDict.copy()

    goal_x, goal_y = base_env.lx, base_env.ly

    print(f"--- INÍCIO DA SIMULAÇÃO ---")
    print(f"Mapa: {MAP_W}x{MAP_H} | Paredes: {len(fixed_items)} | Farol: ({goal_x}, {goal_y})")

    # 2. INICIALIZAR POPULAÇÃO [cite: 153]
    population = [agent_evo.EvoAgent(dna_length=DNA_LENGTH) for _ in range(POP_SIZE)]
    archive = []

    # 3. LOOP EVOLUTIVO
    for gen in range(GENERATIONS):

        # --- A. AVALIAÇÃO ---
        behaviors = []

        for agent in population:
            # Configurar ambiente headless com as paredes fixas
            env = env_lighthouse.Light_House(None, dummy_stats, width=MAP_W, height=MAP_H, fixed_items=fixed_items)
            env.lx, env.ly = goal_x, goal_y

            # Simular e capturar POSIÇÃO FINAL e PASSOS GASTOS
            final_pos, steps = env.simulate_headless(agent.dna)

            agent.final_pos = final_pos
            agent.steps_taken = steps  # Guardar para cálculo de eficiência
            behaviors.append(final_pos)

        # --- B. CÁLCULO DE NOVIDADE [cite: 133, 235] ---
        for i, agent in enumerate(population):
            # Compara com população atual + arquivo
            all_points = behaviors[:i] + behaviors[i + 1:] + archive

            if not all_points:
                agent.novelty_score = 0
                continue

            dists = [calculate_distance(agent.final_pos, p) for p in all_points]
            dists.sort()

            # Média dos k vizinhos mais próximos
            k_nearest = dists[:K_NEIGHBORS]
            if k_nearest:
                agent.novelty_score = sum(k_nearest) / len(k_nearest)
            else:
                agent.novelty_score = 0

            # Atualizar Arquivo [cite: 141]
            if agent.novelty_score > ARCHIVE_THRESHOLD:
                archive.append(agent.final_pos)

        # --- C. CÁLCULO DE FITNESS (Hybrid: Novelty + Objective + Efficiency) [cite: 177] ---
        max_dist_possible = MAP_W + MAP_H

        for agent in population:
            # 1. Distância ao Farol
            dist_to_goal = abs(agent.final_pos[0] - goal_x) + abs(agent.final_pos[1] - goal_y)

            # 2. Score de Proximidade (Exploração guiada)
            proximity_score = 50 * (1 - (dist_to_goal / max_dist_possible))
            if proximity_score < 0: proximity_score = 0

            # 3. BÓNUS DE SUCESSO E EFICIÊNCIA
            success_bonus = 0
            efficiency_bonus = 0

            if dist_to_goal == 0:
                # Recompensa massiva por encontrar a solução
                success_bonus = 2000.0

                # Recompensa por rapidez: Quanto mais passos sobrarem, melhor.
                # Exemplo: Se gastou 50 de 200 passos -> (200 - 50) * 5 = 750 pontos extra
                steps_saved = DNA_LENGTH - agent.steps_taken
                efficiency_bonus = steps_saved * 5.0

            # Fitness Final
            agent.fitness = agent.novelty_score + proximity_score + success_bonus + efficiency_bonus

        # --- D. ORDENAÇÃO E REPORTING ---
        population.sort(key=lambda x: x.fitness, reverse=True)
        best = population[0]

        # Log detalhado
        status = "BUSCANDO..."
        if best.fitness > 1000: status = "SOLUÇÃO!"

        print(
            f"Gen {gen + 1:03}: Fit={best.fitness:.1f} | Steps={best.steps_taken} | Nov={best.novelty_score:.1f} | {status}")

        # --- E. REPRODUÇÃO  ---

        # Elitismo: Top 5 passa direto
        num_elites = 5
        next_gen = population[:num_elites]

        # Seleção de pais (Top 50%)
        parents_pool = population[:POP_SIZE // 2]

        while len(next_gen) < POP_SIZE:
            parent_a = random.choice(parents_pool)
            parent_b = random.choice(parents_pool)

            # Crossover
            child = parent_a.crossover(parent_b)

            # Mutação
            child.mutate(mutation_rate=0.05)

            next_gen.append(child)

        population = next_gen

    # --- 4. VISUALIZAÇÃO FINAL ---
    print("\n--- FIM DO TREINO ---")

    # Reordenar para pegar o campeão absoluto da última geração
    population.sort(key=lambda x: x.fitness, reverse=True)
    champion = population[0]

    print(f"CAMPEÃO: {champion.steps_taken} passos (Fitness: {champion.fitness:.2f})")
    print("A abrir janela do Pygame...")

    visual_env = env_lighthouse.Light_House(
        None,
        dummy_stats,
        width=MAP_W,
        height=MAP_H,
        fixed_items=fixed_items
    )
    visual_env.lx, visual_env.ly = goal_x, goal_y

    visual_env.visualize_agent(champion.dna)

if __name__ == "__main__":
    main()