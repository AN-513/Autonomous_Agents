from Classes import agent, stats
from Envoirments import env_lighthouse

if __name__ == "__main__":
    from Classes import agent
    agent = agent.Agent()
    clusterStats = stats.StatsCluster()
    for _ in range(10):
        stats = stats.Stats()
        env = env_lighthouse.Light_House(agent=agent, stats=stats, light_reach=100, width=5, height=5, num_walls=5)
        env.display_gui()
        stats.print()
        print()
        clusterStats.add_stats(stats)

    clusterStats.display_plots()
    clusterStats.display_heatmap()



