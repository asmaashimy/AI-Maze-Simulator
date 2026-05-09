import time
from collections import deque

with open("simple.txt", "r") as f:
    lines = f.readlines()

MAZE = []
for line in lines:
    row = [int(x) for x in line.strip().split()]
    MAZE.append(row)

ROWS = len(MAZE)
COLS = len(MAZE[0])
START = (0, 0)
GOAL = (ROWS - 1, COLS - 1)

stack = deque([START])
came_from = {START: None}
visited_order = []
nodes_explored = 0

start_time = time.time()

while stack:
    current = stack.pop()
    visited_order.append(current)
    nodes_explored += 1

    if current == GOAL:
        break

    r, c = current
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] == 0:
            neighbor = (nr, nc)
            if neighbor not in came_from:
                stack.append(neighbor)
                came_from[neighbor] = current

end_time = time.time()

path = []
if GOAL in came_from:
    node = GOAL
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()

grid = [row[:] for row in MAZE]
for r, c in path:
    grid[r][c] = "*"

print("\nSolved Maze:")
for row in grid:
    print(" ".join(str(x) for x in row))

print("--- DFS Results ---")
print(f"Path Length: {len(path) - 1}")
print(f"Nodes Explored: {nodes_explored}")
print(f"Time Taken: {end_time - start_time} seconds")
