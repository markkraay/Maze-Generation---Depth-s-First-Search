import pygame
import random
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
width = 500
height = 500
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Generator")


def time_function(func):
    def wrapper(*args):
        start = time.time()
        func(*args)
        time_diff = time.time() - start
        print(time_diff)
    return wrapper


class Maze:
    def __init__(self, dimension):
        self.dimension = dimension
        self.maze = []
        numb = 1
        for _ in range(self.dimension):
            row = []
            for _ in range(self.dimension):
                row.append(numb)
                numb += 1
            self.maze.append(row)
        self.lenMaze = int(dimension ** 2)
        self.visited = []
        self.stack = [[0, 0]]  # Stack list must take list indices.
        self.choices = [1, 2, 3, 4]
        self.pathway = []
        self.column_width = int(width / self.dimension)
        self.row_height = int(height / self.dimension)
        self.short = self.column_width - 5
        self.long = (self.column_width * 2) - 5
        if dimension < 10:
            self.FPS = 1
        elif 10 <= dimension < 30:
            self.FPS = .8
        elif 30 <= dimension < 50:
            self.FPS = .5
        elif 50 <= dimension < 70:
            self.FPS = .2
        elif 70 <= dimension:
            self.FPS = 0

        #   Initialize Screen
        screen.fill(WHITE)


class RecursiveBacktracking(Maze):
    def shift_cube(self, current_cell, new_cell):
        prev_x = current_cell[0]
        prev_y = current_cell[1]
        new_x = new_cell[0]
        new_y = new_cell[1]
        shift_x = new_x - prev_x
        shift_y = new_y - prev_y
        if shift_x == 1:
            pygame.draw.rect(screen, RED, (prev_x * self.column_width + 3, prev_y * self.row_height + 3, self.long,
                                           self.short))
        elif shift_x == -1:
            pygame.draw.rect(screen, RED, ((prev_x - 1) * self.column_width + 3, prev_y * self.row_height + 3, self.long,
                                           self.short))
        elif shift_y == 1:
            pygame.draw.rect(screen, RED, (prev_x * self.column_width + 3, prev_y * self.row_height + 3, self.short, self.long))
        elif shift_y == -1:
            pygame.draw.rect(screen, RED, (prev_x * self.column_width + 3, (prev_y - 1) * self.row_height + 3, self.short,
                                           self.long))
        pygame.display.flip()

    def find_open_space(self, cell):
        pos_y = cell[1]
        pos_x = cell[0]

        if self.maze[pos_y][pos_x] not in self.visited:
            self.visited.append(self.maze[pos_y][pos_x])
        possible_moves = []

        if 0 <= pos_y - 1 < self.dimension and 0 <= pos_x < self.dimension and self.maze[pos_y - 1][pos_x] not in self.visited:
            possible_moves.append(1)
        if 0 <= pos_y < self.dimension and 0 <= pos_x + 1 < self.dimension and self.maze[pos_y][pos_x + 1] not in self.visited:
            possible_moves.append(2)
        if 0 <= pos_y + 1 < self.dimension and 0 <= pos_x < self.dimension and self.maze[pos_y + 1][pos_x] not in self.visited:
            possible_moves.append(3)
        if 0 <= pos_y < self.dimension and 0 <= pos_x - 1 < self.dimension and self.maze[pos_y][pos_x - 1] not in self.visited:
            possible_moves.append(4)

        if len(possible_moves) > 0:
            next_move = random.choice(possible_moves)
            if next_move == 1:
                return [pos_x, pos_y - 1]
            elif next_move == 2:
                return [pos_x + 1, pos_y]
            elif next_move == 3:
                return [pos_x, pos_y + 1]
            elif next_move == 4:
                return [pos_x - 1, pos_y]

        return None

    def carve_path(self, pathway):
        pathway.reverse()
        for i in range(len(pathway) - 1):
            prev_x = pathway[i][0]
            prev_y = pathway[i][1]
            new_x = pathway[i+1][0]
            new_y = pathway[i+1][1]
            shift_x = new_x - prev_x
            shift_y = new_y - prev_y
            if shift_x == 1:
                pygame.draw.rect(screen, BLACK, (prev_x * self.column_width + 3, prev_y * self.row_height + 3, self.long,
                                               self.short))
            elif shift_x == -1:
                pygame.draw.rect(screen, BLACK,
                                 ((prev_x - 1) * self.column_width + 3, prev_y * self.row_height + 3, self.long,
                                  self.short))
            elif shift_y == 1:
                pygame.draw.rect(screen, BLACK,
                                 (prev_x * self.column_width + 3, prev_y * self.row_height + 3, self.short, self.long))
            elif shift_y == -1:
                pygame.draw.rect(screen, BLACK,
                                 (prev_x * self.column_width + 3, (prev_y - 1) * self.row_height + 3, self.short,
                                  self.long))
            pygame.display.flip()
    def run(self):
        while len(self.stack) != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stack.clear()

            current_cell = self.stack.pop(-1)
            new_cell = self.find_open_space(current_cell)
            if not new_cell:
                pass
            else:
                self.stack.append(current_cell)
                self.stack.append(new_cell)
                if new_cell == [self.dimension - 1, self.dimension - 1]:
                    self.pathway = self.stack.copy()
                self.shift_cube(current_cell, new_cell)
        self.carve_path(self.pathway)
        time.sleep(10)
        pygame.quit()


five_maze = RecursiveBacktracking(100)


@time_function
def run_prog():
    five_maze.run()

run_prog()