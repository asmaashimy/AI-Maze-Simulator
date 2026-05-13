import heapq


def run_ucs(MAZE, START, GOAL):
    ROWS = len(MAZE)
    COLS = len(MAZE[0])

    pq = []
    heapq.heappush(pq, (0, START))

    came_from = {START: None}
    cost_so_far = {START: 0}
    visited_order = []

    while pq:
        current_cost, current = heapq.heappop(pq)

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
                new_cost = cost_so_far[current] + 1

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor))
                    came_from[neighbor] = current

    path = []
    if GOAL in came_from:
        node = GOAL
        while node is not None:
            path.append(node)
            node = came_from[node]
        path.reverse()

    return path, visited_order
