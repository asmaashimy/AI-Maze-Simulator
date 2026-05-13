def run_dfs(MAZE, START, GOAL):
    ROWS = len(MAZE)
    COLS = len(MAZE[0])
    
    stack = [START]
    came_from = {START: None}
    visited_order = []

    while stack:
        current = stack.pop()
        
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
                if neighbor not in came_from:
                    stack.append(neighbor)
                    came_from[neighbor] = current

    path = []
    if GOAL in came_from:
        node = GOAL
        while node is not None:
            path.append(node)
            node = came_from[node]
        path.reverse()
    
    return path, visited_order