from Classes import stats, agent
from Envoirments import env_lighthouse

if __name__ == "__main__":
    _randomAgent = agent.RandomAgent()
    _agent = agent.Agent(_randomAgent)
    clusterStats = stats.StatsCluster()
    for _ in range(10):
        _stats = stats.Stats()
        env = env_lighthouse.Light_House(agent=_agent, stats=_stats, light_reach=100, dimensions=(7, 7), num_walls=5)
        env.display_gui()
        _stats.print()
        print()
        clusterStats.add_stats(_stats)

    clusterStats.display_plots()
    clusterStats.display_heatmap()

'''
    if __name__ == "__main__":
        from Classes import agent
        my_agent = agent.Agent()
        clusterStats = stats.StatsCluster()

        w = 5
        h = 5
        walls = 12

        for i in range(5):
            st = stats.Stats()

            # Cria o ambiente
            env = env_lighthouse.Light_House(
                agent=my_agent,
                stats=st,
                light_reach=100,
                width=w,
                height=h,
                num_walls=walls
            )

            env.display_gui()
'''






