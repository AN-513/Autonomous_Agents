from Classes import stats, agent
from Envoirments import env_lighthouse

if __name__ == "__main__":
    _agent = agent.Agent()
    clusterStats = stats.StatsCluster()
    for _ in range(10):
        _stats = stats.Stats()
        env = env_lighthouse.Light_House(agent=_agent, stats=_stats, light_reach=100, width=5, height=5, num_walls=5)
        env.display_gui()
        _stats.print()
        print()
        clusterStats.add_stats(_stats)

    clusterStats.display_plots()
    clusterStats.display_heatmap()



