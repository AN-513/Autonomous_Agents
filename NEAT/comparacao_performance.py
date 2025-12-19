import random
import pickle
import os
import numpy as np
from Envoirments import env_lighthouse
from Classes import agent, stats, sensor

# Configurações globais
MEMORY_SIZE = 10
MAP_SIZE = (15, 15)
NUM_EPISODIOS_ANALISE = 20
PAREDES = 25


def get_sensors():
    return [
        sensor.Sensor(sensor.DirectionSensor("lighthouse_pos")),
        sensor.Sensor(sensor.WallSensor(2)),
        sensor.LightSensor()
    ]


def correr_estatisticas(bot, episodes, walls):
    passos = []
    for _ in range(episodes):
        st = stats.Stats()
        env = env_lighthouse.Light_House(bot, st, 3, dimensions=MAP_SIZE, num_walls=walls, max_steps=200,
                                         random_seed=random.randint(1, 999999))
        res = env.run()  # Execução rápida sem GUI
        passos.append(res[0])
    return np.mean(passos)


if __name__ == "__main__":
    # --- 1. PREPARAÇÃO DOS AGENTES ---
    with open('best_agent.pkl', 'rb') as f:
        neat_bot = pickle.load(f)

    simple_bot = agent.Agent(agent.GreedyFixedAgent(MEMORY_SIZE), get_sensors(), MEMORY_SIZE)
    smart_bot = agent.Agent(agent.SmartGreedyFixedAgent(MEMORY_SIZE), get_sensors(), MEMORY_SIZE)

    # --- 2. ANÁLISE DE PERFORMANCE ---
    print(f"A processar análise estatística ({NUM_EPISODIOS_ANALISE} episódios)...")
    m_simple = correr_estatisticas(simple_bot, NUM_EPISODIOS_ANALISE, PAREDES)
    m_smart = correr_estatisticas(smart_bot, NUM_EPISODIOS_ANALISE, PAREDES)
    m_neat = correr_estatisticas(neat_bot, NUM_EPISODIOS_ANALISE, PAREDES)

    print("\n" + "=" * 40)
    print("MÉDIA DE PASSOS (DADOS RECOLHIDOS)")
    print("=" * 40)
    print(f"Greedy Simples: {m_simple:.2f}")
    print(f"Smart Greedy:   {m_smart:.2f}")
    print(f"Agente NEAT:    {m_neat:.2f}")
    print("=" * 40 + "\n")

    # --- 3. VISUALIZAÇÃO GUI ---
    print("A iniciar demonstração visual no mesmo mapa...")
    SEED_DEMO = random.randint(0, 999999)

    agentes_demo = [
        (simple_bot, "Greedy Simples (Fixa)"),
        (smart_bot, "Smart Greedy (Fixa)"),
        (neat_bot, "Agente NEAT (Aprendida)")
    ]

    for bot, nome in agentes_demo:
        print(f"A mostrar: {nome}")
        # Criar ambiente com GUI para observação
        env = env_lighthouse.Light_House(bot, None, 3, dimensions=MAP_SIZE, num_walls=PAREDES, max_steps=200,
                                         random_seed=SEED_DEMO)
        env.display_gui()