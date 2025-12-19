import random
from Envoirments import env_lighthouse
from Classes import agent, sensor

# 1. Instanciar a política fixa
pure_fixed_policy = agent.GreedyFixedAgent()

# 2. Configurar os mesmos sensores que o NEAT usa para ser uma comparação justa
def get_sensors():
    return [
        sensor.Sensor(sensor.DirectionSensor("lighthouse_pos")),
        sensor.Sensor(sensor.WallSensor(2)),
        sensor.LightSensor()
    ]

# 3. Envolver no wrapper Agent (necessário para processar os sensores)
# Definimos memory_size=0 pois a política fixa raramente precisa de memória anterior
fixed_bot = agent.Agent(pure_fixed_policy, get_sensors(), memory_size=0)

# 4. Correr o ambiente com GUI para observar o comportamento
env = env_lighthouse.Light_House(
    agent=fixed_bot,
    stats=None,
    light_reach=3,
    dimensions=(15, 15),
    num_walls=15,
    max_steps=200,
    random_seed=random.randint(0, 9999)
)

env.display_gui()