import time
import heapq

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

pq = []
heapq.heappush(pq, (0, START))

came_from = {START: None}
cost_so_far = {START: 0}
visited_order = []
nodes_explored = 0

start_time = time.time()

while pq:
    current_cost, current = heapq.heappop(pq)
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
            new_cost = current_cost + 1

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                heapq.heappush(pq, (priority, neighbor))
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

print("--- UCS Results ---")
print(f"Path Length: {len(path) - 1}")
print(f"Nodes Explored: {nodes_explored}")
print(f"Time Taken: {end_time - start_time} seconds")
