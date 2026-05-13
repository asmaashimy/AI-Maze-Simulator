import heapq
import math

def manhattan(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def euclidean(current, goal):
    return math.sqrt((current[0] - goal[0])**2 + (current[1] - goal[1])**2)

def a_star(MAZE, START, GOAL, heuristic_func):
    ROWS = len(MAZE)
    COLS = len(MAZE[0])
    
    pq = []
    h_start = heuristic_func(START, GOAL)
    heapq.heappush(pq, (h_start, START))
    
    came_from = {START: None}
    cost_so_far = {START: 0}
    visited_order = []

    while pq:
        current_f, current = heapq.heappop(pq)
        
        if current not in visited_order:
            visited_order.append(current)

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
                    f = new_g + heuristic_func(neighbor, GOAL)
                    heapq.heappush(pq, (f, neighbor))
                    came_from[neighbor] = current

    path = []
    if GOAL in came_from:
        node = GOAL
        while node is not None:
            path.append(node)
            node = came_from[node]
        path.reverse()
        
    return path, visited_order, 0