import pygame
import sys
import random
import time
from Classes import Agent, Stats


class Light_House:
    def __init__(self, agent:Agent.Agent, stats:Stats.Stats, light_reach:int = 3, width:int = 10, height:int = 10):
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

    def is_agent_lit(self):
        dx = abs(self.agent_x - self.lx)
        dy = abs(self.agent_y - self.ly)
        return dx <= self.light_reach and dy <= self.light_reach

    def is_time_to_move(self):
        #now = time.time()
        #if now - self.last_move_time < 0.1:
        #    return False
        #self.last_move_time = now
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
                valid_decision = True
                self.agent_x, self.agent_y = new_x, new_y
                self.stats.insert_cord((new_x, new_y))

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

            pygame.display.flip()

            if (self.agent_x == self.lx) and (self.agent_y == self.ly):
                running = False
                print("Agent finished envoirment")

        pygame.quit()

