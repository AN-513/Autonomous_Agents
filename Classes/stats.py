from matplotlib import pyplot as plt
import numpy as np

class Stats:
    def __init__(self):
        self.num_decisions = 0
        self.map_dimensions = (-1, -1)  # tuple(width, height)
        self.cords_all = []
        self.i_distance = -1

    def set_map_dimensions(self, map_dimensions: tuple):
        if self.map_dimensions != (-1, -1):
            # print("\nWARNING (stats.py): MAP DIMENSIONS ALREADY SET\n")
            pass
        self.map_dimensions = map_dimensions

    def set_i_distance(self, distance: int):
        self.i_distance = distance

    def increment_decision(self):
        self.num_decisions += 1

    def insert_cord(self, cord: tuple):
        self.cords_all.append(cord)

    def print(self):
        print("\n----- Stats -----")
        print(f"Number of decisions: {self.num_decisions}")
        print(f"Map size: {self.map_dimensions[0] * self.map_dimensions[1]}")
        print(f"Map dimensions: {self.map_dimensions}")
        print(f"Initial distance: {self.i_distance}")

    def get_stats_dict(self):
        dict = {}
        dict["num_decisions"] = self.num_decisions
        dict["map_size"] = self.map_dimensions[0] * self.map_dimensions[1]
        dict["map_dimensions"] = self.map_dimensions
        dict["i_distance"] = self.i_distance
        return dict


class StatsCluster:
    def __init__(self):
        self.stats = []

    def add_stats(self, stats: Stats):
        self.stats.append(stats)

    def display_plots(self):
        x_vals = [s.i_distance for s in self.stats]
        y_vals = [s.num_decisions for s in self.stats]

        if len(x_vals) == 0:
            print("No stats to plot.")
            return

        plt.figure()
        plt.scatter(x_vals, y_vals)

        plt.xlabel("i_distance")
        plt.ylabel("num_decisions")
        plt.title("Initial Distance vs Number of Decisions")

        plt.grid(True)
        plt.show()

    def display_heatmap(self):
        if len(self.stats) == 0:
            print("No stats in cluster.")
            return

        # Assume all stats have the same map dimensions
        w, h = self.stats[0].map_dimensions
        if (w, h) == (-1, -1):
            print("Map dimensions not set in Stats objects.")
            return

        # Create empty global heatmap
        heat = np.zeros((h, w), dtype=int)

        # Sum all coordinates from all stats
        for s in self.stats:
            for (x, y) in s.cords_all:
                if 0 <= x < w and 0 <= y < h:
                    heat[y, x] += 1

        # Plot heatmap
        plt.figure(figsize=(6, 6))
        plt.imshow(heat, cmap="hot", origin="lower")
        plt.colorbar(label="Frequência")
        plt.title("Heatmap combinado de todos os Stats")
        plt.xlabel("X")
        plt.ylabel("Y")

        plt.show()
