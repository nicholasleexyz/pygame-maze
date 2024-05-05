import random
import numpy as np
import sys
import pygame


def generate_maze(row, column, cell_size) -> np.ndarray[np.int32, np.ndim(2)]:
    maze = np.ones((column, row), dtype=int)
    maze[1::2, 1::2] = 0  # clear each room

    stack = [(1, 1)]

    visited = set()
    visited.add((1, 1))

    while stack:
        current = stack[-1]
        directions = {(0, -2), (2, 0), (0, 2), (-2, 0)}

        potential_neighbors = [
            (current[0] + _direction[0], current[1] + _direction[1])
            for _direction in directions]

        valid_neighbors = [n for n in potential_neighbors
                           if 0 <= n[0] < column and 0 <= n[1] < row]

        unvisited = [vn for vn in valid_neighbors if vn not in visited]

        if unvisited:
            neighbor = random.choice(unvisited)
            wall = ((current[0] + neighbor[0]) // 2,
                    (current[1] + neighbor[1]) // 2)
            maze[wall[0], wall[1]] = 0
            visited.add(neighbor)
            stack.append(neighbor)
        else:
            stack.pop()

    scaled_maze = np.kron(maze, np.ones((cell_size, cell_size), dtype=int))

    return scaled_maze


WIDTH = 1024
HEIGHT = 1024
FPS = 30

pygame.init()
pygame.mixer.init()  # For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()  # For syncing the FPS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def main():
    running = True
    drawn = False

    column, row = 65, 65
    cell_size = 3
    maze = generate_maze(column, row, cell_size)
    tile_size = 5

    while running:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((127, 127, 127))

        for y in range(1, maze.shape[0]):
            for x in range(1, maze.shape[1]):
                col = BLACK
                if not (maze[x - 1, y]) or not (maze[x, y - 1]):
                    col = WHITE
                pygame.draw.rect(screen, col, pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
