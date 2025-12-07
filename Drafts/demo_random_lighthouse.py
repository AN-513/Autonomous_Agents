from Classes import Agent, Stats
from Envoirments import env_lighthouse

if __name__ == "__main__":
    from Classes import Agent
    agent = Agent.Agent()
    clusterStats = Stats.StatsCluster()
    for _ in range(20):
        stats = Stats.Stats()
        env = env_lighthouse.Light_House(agent=agent, stats=stats, light_reach=100, width=6, height=6)
        env.display_gui()
        stats.print()
        print()
        clusterStats.add_stats(stats)

    clusterStats.display_plots()



