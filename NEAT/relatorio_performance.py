import random
import pickle
import numpy as np
import matplotlib.pyplot as plt
from Envoirments import env_lighthouse
from Classes import agent, stats, sensor

# Configurações globais
MEMORY_SIZE = 10
MAP_SIZE = (15, 15)
NUM_EPISODIOS = 30  # Aumentado para melhor consistência estatística
PAREDES = 25


def get_sensors():
    return [
        sensor.Sensor(sensor.DirectionSensor("lighthouse_pos")),
        sensor.Sensor(sensor.WallSensor(2)),
        sensor.LightSensor()
    ]


def recolher_dados(bot, episodes, walls, seeds):
    cluster = stats.StatsCluster()
    passos_lista = []

    for i in range(episodes):
        st = stats.Stats()
        # Usamos a mesma semente para os 3 agentes no mesmo índice de episódio
        env = env_lighthouse.Light_House(bot, st, 3, dimensions=MAP_SIZE,
                                         num_walls=walls, max_steps=200,
                                         random_seed=seeds[i])
        num_decisoes, _, _ = env.run()
        cluster.add_stats(st)
        passos_lista.append(num_decisoes)

    return passos_lista, cluster


if __name__ == "__main__":
    # 1. Preparação dos Agentes
    with open('best_agent.pkl', 'rb') as f:
        neat_bot = pickle.load(f)

    simple_bot = agent.Agent(agent.GreedyFixedAgent(MEMORY_SIZE), get_sensors(), MEMORY_SIZE)
    smart_bot = agent.Agent(agent.SmartGreedyFixedAgent(MEMORY_SIZE), get_sensors(), MEMORY_SIZE)

    # 2. Execução (Mesmas sementes para todos)
    seeds = [random.randint(1, 999999) for _ in range(NUM_EPISODIOS)]

    print("A avaliar agentes...")
    data_simple, cluster_simple = recolher_dados(simple_bot, NUM_EPISODIOS, PAREDES, seeds)
    data_smart, cluster_smart = recolher_dados(smart_bot, NUM_EPISODIOS, PAREDES, seeds)
    data_neat, cluster_neat = recolher_dados(neat_bot, NUM_EPISODIOS, PAREDES, seeds)

    # --- 3. IMPLEMENTAÇÃO DOS GRÁFICOS PARA O RELATÓRIO ---

    # A. Bar Chart & Box Plot (Comparação de Eficiência e Robustez)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    labels = ['Simple Greedy', 'Smart Greedy', 'NEAT']
    all_data = [data_simple, data_smart, data_neat]

    # Bar Chart (Médias)
    means = [np.mean(d) for d in all_data]
    ax1.bar(labels, means, color=['red', 'orange', 'green'])
    ax1.set_title("Média de Passos (Eficiência)")
    ax1.set_ylabel("Número de Decisões")

    # Box Plot (Distribuição)
    ax2.boxplot(all_data, tick_labels=labels)
    ax2.set_title("Distribuição de Passos (Robustez)")

    plt.tight_layout()
    plt.show()

    # B. Scatter Plots (Escalabilidade) - Usando o método existente na classe Stats
    print("\nExibindo Gráficos de Escalabilidade (Distância vs Passos)...")
    # Podes correr para o NEAT para ver como ele escala
    cluster_neat.display_plots()

    # C. Heatmaps (Exploração Comportamental)
    print("\nExibindo Heatmaps de Exploração...")
    # O heatmap mostra as zonas de 'congestionamento' (onde ficam presos)
    print("Heatmap: Smart Greedy")
    cluster_smart.display_heatmap()

    print("Heatmap: NEAT")
    cluster_neat.display_heatmap()