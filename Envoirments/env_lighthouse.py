import pygame
import sys
import random
import time
from Classes import agent, stats, items

def coords_to_key(x:int, y:int):
    return str(x) + "-" + str(y)

def key_to_coords(key:str):
    raw_numbers = key.split("-")
    numeric_list = []
    for n in raw_numbers:
        numeric_list.append(int(n))
    return numeric_list


class Light_House:
    def __init__(self, agent:agent.Agent, stats:stats.Stats, light_reach:int = 3, width:int = 10, height:int = 10, num_walls:int = 0):
        pygame.init()

        self.width = width
        self.height = height
        self.tile_size = 40
        self.light_reach = light_reach
        self.agent = agent
        self.stats = stats

        self.window = pygame.display.set_mode((self.width * self.tile_size, self.height * self.tile_size))
        pygame.display.set_caption("Static-Light Lighthouse Grid")

        self.clock = pygame.time.Clock()

        # Random lighthouse position
        self.lx = random.randint(0, width - 1)
        self.ly = random.randint(0, height - 1)

        # Agent starting position
        self.agent_x = width // 2
        self.agent_y = height - 2

        self.stats.set_map_dimensions((width, height))
        self.stats.set_i_distance(abs(self.agent_x - self.lx) + abs(self.agent_y - self.ly))

        # Timer for movement
        self.last_move_time = time.time()

        # --- add items ---

        self.itemsDict = {}

        # add walls
        if num_walls >= height*width - 2:
            print(f"WARNING (env_lighthouse.py): TOO MANY WALLS ({num_walls}) FOR THE MAP SIZE ({height*width}) - TWO SQUARES ARE RESERVED")
            time.sleep(10)

        # --- LÓGICA DE GERAÇÃO DE MAPA VÁLIDO ---
        map_is_valid = False
        attempts = 0

        while not map_is_valid:
            attempts += 1
            self.itemsDict = {}  # Resetar dicionário de itens a cada tentativa
            wall_counter = 0

            while wall_counter < num_walls:
                x_wall = random.randint(0, width-1)
                y_wall = random.randint(0, height-1)

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
                self.itemsDict[coords_to_key(x_wall, y_wall)] = items.Item(name="Wall")
                wall_counter += 1

            # VERIFICAÇÃO CRÍTICA: Existe caminho?
            if self.check_path_exists():
                map_is_valid = True

                print(f"Mapa válido gerado na tentativa {attempts}")
            else:
                # Se falhar, o loop repete, apaga o itemsDict e tenta outra configuração
                print(f"X Mapa inválido. Tentativa {attempts}...")
                self.debug_print_map_tui()
                pass


    def debug_print_map_tui(self):
        # Percorre linha a linha (y)
        for y in range(self.height):
            line_str = "|"

            # Percorre coluna a coluna (x)
            for x in range(self.width):
                key = coords_to_key(x, y)

                if x == self.agent_x and y == self.agent_y:
                    char = " A "  # Agente
                elif x == self.lx and y == self.ly:
                    char = " F "  # Farol
                elif key in self.itemsDict and self.itemsDict[key].blocksPassage:
                    char = "###"  # Parede
                else:
                    char = " . "  # Espaço vazio

                line_str += char

            print(line_str + "|")
        print("-" * (self.width * 3 + 2))

    def is_agent_lit(self):
        dx = abs(self.agent_x - self.lx)
        dy = abs(self.agent_y - self.ly)
        return dx <= self.light_reach and dy <= self.light_reach

    def is_time_to_move(self):
        now = time.time()
        if now - self.last_move_time < 0.1:
            return False
        self.last_move_time = now
        return True

    def agent_decision(self):

        if not self.is_time_to_move():
            return

        self.stats.increment_decision()

        # Random direction: up/down/left/right
        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        valid_decision = False

        while not valid_decision:
            dx, dy = self.agent.make_decision(directions)

            new_x = self.agent_x + dx
            new_y = self.agent_y + dy

            # TODO: ADD MORE CHECKS IN THE FUTURE
            if (new_x >= 0) and (new_x <= self.width-1) and (new_y >= 0) and (new_y <= self.height-1):
                # checking wall colision
                if coords_to_key(new_x, new_y) in self.itemsDict:
                    if self.itemsDict[coords_to_key(new_x, new_y)].blocksPassage:
                        continue    # not a valid move

                valid_decision = True
                self.agent_x, self.agent_y = new_x, new_y
                self.stats.insert_cord((new_x, new_y))

    def check_path_exists(self):
        # Fila para o algoritmo BFS: guarda tuplos (x, y)
        queue = [(self.agent_x, self.agent_y)]

        # Conjunto de visitados para não entrar em loops
        visited = set()
        visited.add((self.agent_x, self.agent_y))

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Cima, Baixo, Dir, Esq

        while len(queue) > 0:
            cx, cy = queue.pop(0)  # Retira o primeiro da fila

            # Se chegámos ao farol, o caminho existe
            if cx == self.lx and cy == self.ly:
                return True

            # Verificar vizinhos
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy

                # Verificar limites do mapa
                if 0 <= nx < self.width and 0 <= ny < self.height:

                    #  Verificar se é parede
                    key = coords_to_key(nx, ny)
                    is_blocked = False
                    if key in self.itemsDict and self.itemsDict[key].blocksPassage:
                        is_blocked = True

                    # Se não for parede e ainda não foi visitado, adiciona à fila
                    if not is_blocked and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))

        # Se a fila esvaziar e não encontrámos o farol, não há caminho
        return False

    def run(self):
        running = True
        while running:
            # Agent movement
            self.agent_decision()

            if (self.agent_x == self.lx) and (self.agent_y == self.ly):
                running = False
                print("Agent finished envoirment")


    def display_gui(self):
        running = True

        while running:
            self.clock.tick(20)  # FPS rendering

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Agent movement
            self.agent_decision()

            # Draw background
            self.window.fill((40, 40, 40))

            # Draw grid
            for x in range(self.width):
                for y in range(self.height):
                    pygame.draw.rect(self.window, (70, 70, 70), (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size), 1)

            # Draw light area
            for x in range(self.width):
                for y in range(self.height):
                    if abs(x - self.lx) <= self.light_reach and abs(y - self.ly) <= self.light_reach:
                        pygame.draw.rect(self.window, (255, 255, 180), (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))

            # Draw lighthouse
            pygame.draw.rect(
                self.window,(255, 100, 0),(self.lx * self.tile_size, self.ly * self.tile_size, self.tile_size, self.tile_size))

            # Draw agent
            color = (0, 255, 0) if self.is_agent_lit() else (0, 0, 255)
            pygame.draw.rect(self.window, color, (self.agent_x * self.tile_size, self.agent_y * self.tile_size, self.tile_size, self.tile_size))

            # Draw walls
            color = (200, 50, 100)
            for k, v in self.itemsDict.items():
                if v.name == "Wall":
                    coords = key_to_coords(k)
                    pygame.draw.rect(self.window, color, (coords[0]*self.tile_size, coords[1]*self.tile_size, self.tile_size, self.tile_size))

            pygame.display.flip()

            if (self.agent_x == self.lx) and (self.agent_y == self.ly):
                running = False
                print("Agent finished envoirment")

        pygame.quit()



