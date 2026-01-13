import sys
import random
import time
from Classes import agent, stats, items
from Envoirments.aux_funcs import *


class Light_House_Maze:
    def __init__(self, agent:agent.Agent, stats:stats.Stats, light_reach:int = 3, dimensions:tuple=(7, 7), num_walls:int = 0,
                 max_steps:int = 200, random_seed:int=0):

        self.width = dimensions[0]
        self.height = dimensions[1]
        self.tile_size = 30
        self.light_reach = light_reach
        self.agent = agent
        self.stats = stats
        self.map_validity = True
        self.i_distance = -1

        self.max_steps = max_steps
        self.discovered_positions = []

        random.seed(random_seed)

        self.generate_map(num_walls=num_walls, prevent_spawn_in_light=False)
        while not self.map_validity:
            self.map_validity = True
            self.generate_map(num_walls=num_walls, prevent_spawn_in_light=False)


    def generate_map(self, num_walls:int, prevent_spawn_in_light:bool):

        # Random lighthouse position
        self.lx = random.randint(0, self.width - 1)
        self.ly = random.randint(0, self.height - 1)

        # Agent starting position
        self.agent_x = random.randint(0, self.width - 1)
        self.agent_y = random.randint(0, self.height - 1)

        self.discovered_positions.append(coords_to_key(self.agent_x, self.agent_y))

        contador = 0

        while (self.agent_x == self.lx and self.agent_y == self.ly) or (self.is_agent_lit() and prevent_spawn_in_light):
            contador += 1
            if contador >= 1000:
                self.map_validity = False
                return
            self.agent_x = random.randint(0, self.width - 1)
            self.agent_y = random.randint(0, self.height - 1)

        if self.stats:
            self.stats.set_map_dimensions((self.width, self.height))
            self.stats.set_i_distance(abs(self.agent_x - self.lx) + abs(self.agent_y - self.ly))

        # Timer for movement
        self.last_move_time = time.time()

        # --- add items ---

        self.itemsDict = {}

        # add walls
        if num_walls >= self.height * self.width - 2:
            print(
                f"WARNING (envoirment.py): TOO MANY WALLS ({num_walls}) FOR THE MAP SIZE ({self.height * self.width}) - TWO SQUARES ARE RESERVED")
            time.sleep(10)

        # --- LÓGICA DE GERAÇÃO DE MAPA VÁLIDO ---
        map_is_valid = False
        attempts = 0

        while not map_is_valid:
            attempts += 1
            self.itemsDict = {}  # Resetar dicionário de itens a cada tentativa
            wall_counter = 0

            while wall_counter < num_walls:
                x_wall = random.randint(0, self.width - 1)
                y_wall = random.randint(0, self.height - 1)

                # check lighthouse colision
                if x_wall == self.lx and y_wall == self.ly:
                    continue

                # check agent initial position colision:
                if x_wall == self.agent_x and y_wall == self.agent_y:
                    continue

                # check if wall is on top of another wall
                if coords_to_key(x_wall, y_wall) in self.itemsDict:
                    continue

                # all checks passed - adding wall
                self.itemsDict[coords_to_key(x_wall, y_wall)] = items.Item(name="Wall", coordinates=(x_wall, y_wall))
                wall_counter += 1

            if self.check_path_exists():
                map_is_valid = True

        if self.stats:
            self.stats.set_num_walls(num_walls)
        self.i_distance = calc_distance(self.agent_x, self.agent_y, self.lx, self.ly)

    def is_map_valid(self):
        return self.map_validity

    def is_agent_lit(self):
        dx = abs(self.agent_x - self.lx)
        dy = abs(self.agent_y - self.ly)
        return dx <= self.light_reach and dy <= self.light_reach

    def is_time_to_move(self):
        now = time.time()
        if now - self.last_move_time < 0.05:
            return False
        self.last_move_time = now
        return True

    def agent_decision(self, skip_time_delay:bool):

        if (not skip_time_delay) and not(self.is_time_to_move()):
            return

        if self.stats:
            self.stats.increment_decision()

        # Random direction: up/down/left/right
        options = [(1,0), (-1,0), (0,1), (0,-1)]

        valid_decision = False

        obs_dict = {}

        # direção relativa do farol
        obs_dict["lighthouse_pos"] = (self.lx, self.ly)
        obs_dict["agent_pos"] = (self.agent_x, self.agent_y)
        obs_dict["env_size"] = (self.width, self.height)
        obs_dict["items_dict"] = self.itemsDict
        obs_dict["light_intensity"] = 0
        if self.is_agent_lit():
            obs_dict["light_intensity"] = (self.light_reach + 1 - calc_distance(self.agent_x, self.agent_y, self.lx, self.ly)) / (1+self.light_reach)


        # check valid decisions
        invalid_options = []

        for i in range(len(options)):
            option = options[i]
            new_x = self.agent_x + option[0]
            new_y = self.agent_y + option[1]

            if (new_x >= 0) and (new_x <= self.width - 1) and (new_y >= 0) and (new_y <= self.height - 1):
                # checking wall colision
                if coords_to_key(new_x, new_y) in self.itemsDict:
                    if self.itemsDict[coords_to_key(new_x, new_y)].blocksPassage:
                        invalid_options.append(option)
            else:
                invalid_options.append(option)


        valid_options_exist = False
        for option in options:
            if option not in invalid_options:
                valid_options_exist = True
                break

        if not valid_options_exist:
            self.save_debug_frame("no_valid_decisions.png")

        first_run = True
        while not valid_decision:
            if first_run:
                decision = self.agent.make_decision(options=options, observations=obs_dict, invalid_options=invalid_options)
                first_run = False
            else:
                decision = random.choice(options)
                print("Warning (envoirment.py): Random decision")

            dx, dy = decision
            self.agent.add_decision_to_memory(options.index(tuple(decision)))

            new_x = self.agent_x + dx
            new_y = self.agent_y + dy

            if (new_x >= 0) and (new_x <= self.width-1) and (new_y >= 0) and (new_y <= self.height-1):
                # checking wall colision
                if coords_to_key(new_x, new_y) in self.itemsDict:
                    if self.itemsDict[coords_to_key(new_x, new_y)].blocksPassage:
                        continue    # not a valid move

                valid_decision = True
                self.agent_x, self.agent_y = new_x, new_y
                pos_key = coords_to_key(self.agent_x, self.agent_y)
                if pos_key not in self.discovered_positions:
                    self.discovered_positions.append(pos_key)
                if self.stats:
                    self.stats.insert_coord((new_x, new_y))
                break


    def check_path_exists(self):
        queue = [(self.agent_x, self.agent_y)]
        visited = set()
        visited.add((self.agent_x, self.agent_y))

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while len(queue) > 0:
            cx, cy = queue.pop(0)
            if cx == self.lx and cy == self.ly:
                return True
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    key = coords_to_key(nx, ny)
                    is_blocked = False
                    if key in self.itemsDict and self.itemsDict[key].blocksPassage:
                        is_blocked = True

                    if not is_blocked and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
        return False

    def run(self):
        running = True

        num_decisions = 0

        while running:
            num_decisions += 1
            # Agent movement
            self.agent_decision(skip_time_delay=True)

            if (self.agent_x == self.lx) and (self.agent_y == self.ly):
                running = False

            if num_decisions >= self.max_steps:
                break

        distance_to_lighthouse = calc_distance(self.agent_x, self.agent_y, self.lx, self.ly)
        if distance_to_lighthouse == 0 and self.stats:
            self.stats.set_as_win()
        return (num_decisions, distance_to_lighthouse, len(self.discovered_positions))

    def display_gui(self):
        import pygame
        pygame.init()

        self.window = pygame.display.set_mode(
            (self.width * self.tile_size, self.height * self.tile_size)
        )

        base_title = "Static-Light Lighthouse Grid"
        pygame.display.set_caption(base_title)

        self.clock = pygame.time.Clock()
        running = True
        num_decisions = 0

        while running:
            self.clock.tick(10)  # FPS rendering

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Agent movement
            self.agent_decision(skip_time_delay=False)
            num_decisions += 1

            # 🔹 UPDATE WINDOW TITLE
            pygame.display.set_caption(
                f"{base_title} - [{num_decisions}]"
            )

            # Draw background
            self.window.fill((40, 40, 40))

            # Draw grid
            for x in range(self.width):
                for y in range(self.height):
                    pygame.draw.rect(
                        self.window,
                        (70, 70, 70),
                        (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size),
                        1
                    )

            # Draw light area
            for x in range(self.width):
                for y in range(self.height):
                    if abs(x - self.lx) <= self.light_reach and abs(y - self.ly) <= self.light_reach:
                        pygame.draw.rect(
                            self.window,
                            (255, 255, 180),
                            (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                        )

            # Draw walls
            color = (200, 50, 100)
            for k, v in self.itemsDict.items():
                if v.name == "Wall":
                    coords = key_to_coords(k)
                    pygame.draw.rect(
                        self.window,
                        color,
                        (coords[0] * self.tile_size, coords[1] * self.tile_size,
                         self.tile_size, self.tile_size)
                    )

            # Draw lighthouse
            pygame.draw.rect(
                self.window,
                (255, 100, 0),
                (self.lx * self.tile_size, self.ly * self.tile_size,
                 self.tile_size, self.tile_size)
            )

            # Draw agent
            color = (0, 255, 0) if self.is_agent_lit() else (0, 0, 255)
            pygame.draw.rect(
                self.window,
                color,
                (self.agent_x * self.tile_size, self.agent_y * self.tile_size,
                 self.tile_size, self.tile_size)
            )

            pygame.display.flip()

            if num_decisions >= self.max_steps:
                break

            if (self.agent_x == self.lx) and (self.agent_y == self.ly):
                running = False

        distance_to_lighthouse = abs(self.agent_x - self.lx) + abs(self.agent_y - self.ly)
        if distance_to_lighthouse == 0:
            self.stats.set_as_win()
        return (num_decisions, distance_to_lighthouse, len(self.discovered_positions))

    def save_debug_frame(self, filename, draw_history=False):
        import pygame

        pygame.init()
        surface = pygame.Surface((self.width * self.tile_size, self.height * self.tile_size))

        # Background
        surface.fill((40, 40, 40))

        # Grid
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(
                    surface, (70, 70, 70),
                    (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size),
                    1
                )

        # Light area
        for x in range(self.width):
            for y in range(self.height):
                if abs(x - self.lx) <= self.light_reach and abs(y - self.ly) <= self.light_reach:
                    pygame.draw.rect(
                        surface, (255, 255, 180),
                        (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    )

        # === HISTORY OVERLAY ===
        if draw_history:
            for hx, hy in self.agent_position_history:
                pygame.draw.rect(
                    surface, (120, 200, 255),  # light blue
                    (hx * self.tile_size, hy * self.tile_size, self.tile_size, self.tile_size)
                )

        # Lighthouse
        pygame.draw.rect(
            surface, (255, 100, 0),
            (self.lx * self.tile_size, self.ly * self.tile_size, self.tile_size, self.tile_size)
        )

        # Agent
        color = (0, 255, 0) if self.is_agent_lit() else (0, 0, 255)
        pygame.draw.rect(
            surface, color,
            (self.agent_x * self.tile_size, self.agent_y * self.tile_size, self.tile_size, self.tile_size)
        )

        # Walls
        for k, v in self.itemsDict.items():
            if v.name == "Wall":
                x, y = key_to_coords(k)
                pygame.draw.rect(
                    surface, (200, 50, 100),
                    (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                )

        pygame.image.save(surface, filename)
        pygame.quit()


    def get_i_distance(self):
        if self.i_distance == -1:
            print("WARNING (envoirment.py): i_distance not set!")
            time.sleep(5)
        else:
            return self.i_distance
