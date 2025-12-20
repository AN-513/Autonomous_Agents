from matplotlib import pyplot as plt
import numpy as np

class Stats:
    def __init__(self):
        self.num_decisions = 0
        self.map_dimensions = (-1, -1)  # tuple(width, height)
        self.cords_all = []
        self.i_distance = -1
        self.num_walls = 0
        self.won = False

    def set_map_dimensions(self, map_dimensions: tuple):
        if self.map_dimensions != (-1, -1):
            print("\nWARNING (stats.py): MAP DIMENSIONS ALREADY SET\n")
        self.map_dimensions = map_dimensions

    def set_num_walls(self, num_walls:int):
        self.num_walls = num_walls

    def set_i_distance(self, distance: int):
        self.i_distance = distance

    def increment_decision(self):
        self.num_decisions += 1

    def insert_coord(self, coord: tuple):
        self.cords_all.append(coord)

    def set_as_win(self):
        self.won = True

    def print(self):
        print("\n----- Stats -----")
        print(f"Number of decisions: {self.num_decisions}")
        print(f"Map size: {self.map_dimensions[0] * self.map_dimensions[1]}")
        print(f"Map dimensions: {self.map_dimensions}")
        print(f"Initial distance: {self.i_distance}")
        print("Won:", self.won)

    def get_stats_dict(self):
        dict = {}
        dict["num_decisions"] = self.num_decisions
        dict["map_size"] = self.map_dimensions[0] * self.map_dimensions[1]
        dict["map_dimensions"] = self.map_dimensions
        dict["i_distance"] = self.i_distance
        dict["won"] = self.won
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

    def plot_win_rate_by_map_size(self, save_path: str = None):
        """
        Plot the probability of winning a game based on map size.

        Args:
            save_path: Optional file path to save the figure
        """
        if len(self.stats) == 0:
            print("No stats available for plotting.")
            return

        # Group stats by map size
        map_size_dict = {}
        for stat in self.stats:
            w, h = stat.map_dimensions
            map_size = w  # or w*h depending on your preference

            if map_size not in map_size_dict:
                map_size_dict[map_size] = {'wins': 0, 'total': 0}

            map_size_dict[map_size]['total'] += 1
            if stat.won:
                map_size_dict[map_size]['wins'] += 1

        # Calculate win rates
        sizes = sorted(map_size_dict.keys())
        win_rates = []
        for size in sizes:
            wr = (map_size_dict[size]['wins'] / map_size_dict[size]['total'] * 100)
            win_rates.append(round(wr, 2))

        # Create plot
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar([str(s) for s in sizes],
                      win_rates,
                      color='#3498db',
                      edgecolor='#2c3e50',
                      linewidth=1.5)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax.set_xlabel('Map Size (width/height)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Win Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Win Rate by Map Size', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 105)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

    def plot_win_rate_by_num_walls(self, save_path: str = None):
        """
        Plot the probability of winning a game based on number of walls.

        Args:
            save_path: Optional file path to save the figure
        """
        if len(self.stats) == 0:
            print("No stats available for plotting.")
            return

        # Group stats by number of walls
        walls_dict = {}
        for stat in self.stats:
            num_walls = stat.num_walls

            if num_walls not in walls_dict:
                walls_dict[num_walls] = {'wins': 0, 'total': 0}

            walls_dict[num_walls]['total'] += 1
            if stat.won:
                walls_dict[num_walls]['wins'] += 1

        # Calculate win rates
        wall_counts = sorted(walls_dict.keys())
        win_rates = []
        for walls in wall_counts:
            wr = (walls_dict[walls]['wins'] / walls_dict[walls]['total'] * 100)
            win_rates.append(round(wr, 2))

        # Create plot
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar([str(w) for w in wall_counts],
                      win_rates,
                      color='#2ecc71',
                      edgecolor='#27ae60',
                      linewidth=1.5)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax.set_xlabel('Number of Walls', fontsize=12, fontweight='bold')
        ax.set_ylabel('Win Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Win Rate by Number of Walls', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 105)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

