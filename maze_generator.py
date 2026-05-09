import random

maze_types = ["simple", "dense", "corridors", "multiple", "open"]
rows = 20
cols = 20

for m_type in maze_types:
    maze = [[0 for _ in range(cols)] for _ in range(rows)]

    prob = 0.2
    if m_type == "dense":
        prob = 0.4
    elif m_type == "open":
        prob = 0.05
    elif m_type == "corridors":
        for r in range(rows):
            for c in range(cols):
                if r % 2 != 0 and random.random() < 0.8:
                    maze[r][c] = 1
        prob = 0.0
    elif m_type == "multiple":
        prob = 0.25

    if prob > 0:
        for r in range(rows):
            for c in range(cols):
                if random.random() < prob:
                    maze[r][c] = 1

    maze[0][0] = 0
    maze[rows - 1][cols - 1] = 0

    with open(f"{m_type}.txt", "w") as f:
        for row in maze:
            f.write(" ".join(str(x) for x in row) + "\n")
