import time
import heapq
import math

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

def manhattan(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def euclidean(current, goal):
    return math.sqrt((current[0] - goal[0])**2 + (current[1] - goal[1])**2)

def a_star(start, goal, heuristic_func):
    pq = []
    h_start = heuristic_func(start, goal)
    heapq.heappush(pq, (h_start, start))
    
    came_from = {start: None}
    cost_so_far = {start: 0} 
    nodes_explored = 0
    start_time = time.time()

    while pq:
        current_f, current = heapq.heappop(pq)
        nodes_explored += 1

        if current == GOAL:
            break

        r, c = current
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] == 0:
                neighbor = (nr, nc)
                new_g = cost_so_far[current] + 1

                if neighbor not in cost_so_far or new_g < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_g
                    h = heuristic_func(neighbor, goal)
                    f = new_g + h
                    heapq.heappush(pq, (f, neighbor))
                    came_from[neighbor] = current

    end_time = time.time()
    
    path = []
    if GOAL in came_from:
        node = GOAL
        while node is not None:
            path.append(node)
            node = came_from[node]
        path.reverse()
        
    return path, nodes_explored, (end_time - start_time)

print("--- A* with Manhattan Heuristic ---")
path_m, explored_m, time_m = a_star(START, GOAL, manhattan)

grid_m = [row[:] for row in MAZE]
for r, c in path_m:
    grid_m[r][c] = '*'

print("\nSolved Maze (Manhattan):")
for row in grid_m:
    print(' '.join(str(x) for x in row))

print(f"Path Length: {len(path_m) - 1}")
print(f"Nodes Explored: {explored_m}")
print(f"Time Taken: {time_m:.5f} seconds\n")

print("="*30)

print("--- A* with Euclidean Heuristic ---")
path_e, explored_e, time_e = a_star(START, GOAL, euclidean)

grid_e = [row[:] for row in MAZE]
for r, c in path_e:
    grid_e[r][c] = '*'

print("\nSolved Maze (Euclidean):")
for row in grid_e:
    print(' '.join(str(x) for x in row))

print(f"Path Length: {len(path_e) - 1}")
print(f"Nodes Explored: {explored_e}")
print(f"Time Taken: {time_e:.5f} seconds\n")