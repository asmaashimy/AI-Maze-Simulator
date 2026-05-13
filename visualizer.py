import pygame
import sys
import time

import maze_generator
import bfs
import dfs
import ucs
import a_star

# --- الألوان اللي هستخدمها في البروجيكت ---
WIDTH, HEIGHT = 980, 760
BG_COLOR = (235, 235, 235)  # خلفية رمادي فاتح عشان تدي شكل رسمي
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)  # لون الحيطان
BLUE = (52, 152, 219)  # المربعات اللي الخوارزمية بتستكشفها
GREEN = (46, 204, 113)  # مسار الحل النهائي
RED = (231, 76, 60)  # نقطة النهاية (الهدف)
START_COLOR = (155, 89, 182)  # نقطة البداية
BTN_COLOR = (160, 160, 160)  # لون زراير التحكم
TEXT_COLOR = (0, 0, 0)  # لون الكلام
DROP_BG = (255, 255, 255)

# --- ملفات المتاهات الـ 5 اللي جهزناها ---
maze_files = ["simple.txt", "dense.txt", "corridors.txt", "multiple.txt", "open.txt"]
current_maze_idx = 0


def load_maze(filename):
    # بحاول اقرأ المتاهة من الفايل، لو ملقتهوش بعمل واحدة فاضية احتياطي
    try:
        with open(filename, "r") as f:
            return [[int(x) for x in line.split()] for line in f]
    except FileNotFoundError:
        return [[0] * 10 for _ in range(10)]


MAZE = load_maze(maze_files[current_maze_idx])
ROWS, COLS = len(MAZE), len(MAZE[0])
GRID_SIZE = 600
MAZE_X, MAZE_Y = 30, 30
CELL_SIZE = GRID_SIZE // max(ROWS, COLS)

# --- هنا ببدأ اشغل مكتبة Pygame واظبط الشاشة والخطوط ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous Maze-Solving Robot Simulator")
font = pygame.font.SysFont("Arial", 20, bold=True)
small_font = pygame.font.SysFont("Arial", 16)
title_font = pygame.font.SysFont("Arial", 24, bold=True)

# --- تظبيط اماكن واحجام اللوحة اللي على اليمين ---
RIGHT_PANEL_X = 680
BTN_WIDTH = 250
BTN_HEIGHT = 40

algo_buttons = [
    {
        "name": "Breadth-First Search (BFS)",
        "id": "BFS",
        "rect": pygame.Rect(RIGHT_PANEL_X, 120, BTN_WIDTH, BTN_HEIGHT),
    },
    {
        "name": "Depth-First Search (DFS)",
        "id": "DFS",
        "rect": pygame.Rect(RIGHT_PANEL_X, 175, BTN_WIDTH, BTN_HEIGHT),
    },
    {
        "name": "Uniform Cost Search (UCS)",
        "id": "UCS",
        "rect": pygame.Rect(RIGHT_PANEL_X, 230, BTN_WIDTH, BTN_HEIGHT),
    },
    {
        "name": "A* (Manhattan)",
        "id": "A* Manhattan",
        "rect": pygame.Rect(RIGHT_PANEL_X, 285, BTN_WIDTH, BTN_HEIGHT),
    },
    {
        "name": "A* (Euclidean)",
        "id": "A* Euclidean",
        "rect": pygame.Rect(RIGHT_PANEL_X, 340, BTN_WIDTH, BTN_HEIGHT),
    },
]

reset_btn = {
    "name": "Reset Environment",
    "rect": pygame.Rect(RIGHT_PANEL_X, 665, BTN_WIDTH, BTN_HEIGHT),
}

# تظبيط القائمة اللي بختار منها نوع المتاهة
dropdown_rect = pygame.Rect(RIGHT_PANEL_X, 480, BTN_WIDTH, BTN_HEIGHT)
dropdown_active = False
dropdown_options = []
for i, m in enumerate(maze_files):
    dropdown_options.append(pygame.Rect(RIGHT_PANEL_X, 520 + (i * 40), BTN_WIDTH, 40))


# --- الدالة المسؤولة عن رسم كل حاجة على الشاشة ---
def draw_ui(msg, stats, current_visited, current_path):
    screen.fill(BG_COLOR)

    # 1. برسم المتاهة نفسها وبعملها إطار أسود
    pygame.draw.rect(
        screen, WHITE, (MAZE_X - 2, MAZE_Y - 2, GRID_SIZE + 4, GRID_SIZE + 4)
    )
    pygame.draw.rect(
        screen, BLACK, (MAZE_X - 2, MAZE_Y - 2, GRID_SIZE + 4, GRID_SIZE + 4), 2
    )

    for r in range(ROWS):
        for c in range(COLS):
            color = WHITE
            if MAZE[r][c] == 1:
                color = BLACK
            if current_visited and (r, c) in current_visited:
                color = BLUE
            if current_path and (r, c) in current_path:
                color = GREEN
            if (r, c) == (0, 0):
                color = START_COLOR
            if (r, c) == (ROWS - 1, COLS - 1):
                color = RED

            rect = (
                MAZE_X + c * CELL_SIZE,
                MAZE_Y + r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

    # 2. رسم الداشبورد اللي تحت عشان يعرض النتايج
    dash_rect = pygame.Rect(MAZE_X, MAZE_Y + GRID_SIZE + 20, GRID_SIZE, 85)
    pygame.draw.rect(screen, WHITE, dash_rect)
    pygame.draw.rect(screen, BLACK, dash_rect, 2)

    dash_title = font.render("Performance Dashboard", True, TEXT_COLOR)
    screen.blit(dash_title, (dash_rect.x + 20, dash_rect.y + 10))
    pygame.draw.line(
        screen,
        BLACK,
        (dash_rect.x + 20, dash_rect.y + 35),
        (dash_rect.x + 250, dash_rect.y + 35),
        1,
    )

    # لو فيه نتايج اطبعها، لو مفيش حط شرط
    if stats:
        t_nodes = small_font.render(
            f"Nodes Explored: {stats['nodes']}", True, TEXT_COLOR
        )
        t_path = small_font.render(f"Path Length: {stats['length']}", True, TEXT_COLOR)
        t_time = small_font.render(
            f"Time Taken: {stats['time']:.4f} sec", True, TEXT_COLOR
        )
    else:
        t_nodes = small_font.render("Nodes Explored: --", True, TEXT_COLOR)
        t_path = small_font.render("Path Length: --", True, TEXT_COLOR)
        t_time = small_font.render("Time Taken: -- sec", True, TEXT_COLOR)

    screen.blit(t_nodes, (dash_rect.x + 20, dash_rect.y + 45))
    screen.blit(t_path, (dash_rect.x + 220, dash_rect.y + 45))
    screen.blit(t_time, (dash_rect.x + 420, dash_rect.y + 45))

    # 3. برسم لوحة التحكم اللي على اليمين (الزراير)
    title = title_font.render("Control Panel", True, TEXT_COLOR)
    screen.blit(title, (RIGHT_PANEL_X, 30))

    status = font.render(
        msg,
        True,
        (0, 100, 200) if "Completed" in msg or "Loaded" in msg else TEXT_COLOR,
    )
    screen.blit(status, (RIGHT_PANEL_X, 70))

    # برسم زراير الخوارزميات وبحط عليها اساميها
    for btn in algo_buttons:
        pygame.draw.rect(screen, BTN_COLOR, btn["rect"])
        pygame.draw.rect(screen, BLACK, btn["rect"], 1)
        text = small_font.render(btn["name"], True, TEXT_COLOR)
        screen.blit(text, (btn["rect"].x + 10, btn["rect"].y + 10))

    # زرار الريست عشان لو حبيت اصفر الدنيا
    pygame.draw.rect(screen, (200, 80, 80), reset_btn["rect"])
    pygame.draw.rect(screen, BLACK, reset_btn["rect"], 1)
    r_text = font.render(reset_btn["name"], True, WHITE)
    screen.blit(r_text, (reset_btn["rect"].x + 35, reset_btn["rect"].y + 8))

    # 4. رسم القائمة اللي بختار منها نوع المتاهة
    lbl = font.render("Select Environment:", True, TEXT_COLOR)
    screen.blit(lbl, (RIGHT_PANEL_X, 440))

    pygame.draw.rect(screen, WHITE, dropdown_rect)
    pygame.draw.rect(screen, BLACK, dropdown_rect, 1)

    maze_name = maze_files[current_maze_idx].replace(".txt", "").capitalize()
    drop_text = font.render(f"{maze_name} Maze", True, TEXT_COLOR)
    screen.blit(drop_text, (dropdown_rect.x + 10, dropdown_rect.y + 8))

    arrow = font.render("V" if not dropdown_active else "A", True, TEXT_COLOR)
    screen.blit(arrow, (dropdown_rect.x + BTN_WIDTH - 25, dropdown_rect.y + 8))

    if dropdown_active:
        for i, opt_rect in enumerate(dropdown_options):
            pygame.draw.rect(screen, DROP_BG, opt_rect)
            pygame.draw.rect(screen, BLACK, opt_rect, 1)
            opt_name = maze_files[i].replace(".txt", "").capitalize()
            opt_text = small_font.render(f"{opt_name} Maze", True, TEXT_COLOR)
            screen.blit(opt_text, (opt_rect.x + 10, opt_rect.y + 10))


# --- دالة الانيميشن عشان تظهر الخوارزمية وهي بتحل ---
def animate_solution(visited_order, path, algo_time, current_stats):
    current_visited = set()
    for node in visited_order:
        current_visited.add(node)
        draw_ui("Exploring...", current_stats, current_visited, None)
        pygame.display.update()
        pygame.time.delay(20)

    current_path = []
    for node in path:
        current_path.append(node)
        draw_ui("Goal Reached!", current_stats, current_visited, current_path)
        pygame.display.update()
        pygame.time.delay(20)

    return {
        "nodes": len(visited_order),
        "length": len(path) - 1 if path else 0,
        "time": algo_time,
    }


# --- المايسترو اللي بيشغل كل حاجة ---
def main():
    global MAZE, ROWS, COLS, CELL_SIZE, current_maze_idx, dropdown_active

    running = True
    c_visited, c_path, c_stats = None, None, None
    msg = "Awaiting Command..."

    while running:
        draw_ui(msg, c_stats, c_visited, c_path)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = event.pos

                # لو القائمة بتاعت المتاهات مفتوحة وحد اختار حاجة
                if dropdown_active:
                    clicked_option = False
                    for i, opt_rect in enumerate(dropdown_options):
                        if opt_rect.collidepoint(m_pos):
                            current_maze_idx = i
                            MAZE = load_maze(maze_files[current_maze_idx])
                            ROWS, COLS = len(MAZE), len(MAZE[0])
                            CELL_SIZE = GRID_SIZE // max(ROWS, COLS)
                            c_visited, c_path, c_stats = None, None, None
                            msg = "Environment Loaded."
                            clicked_option = True
                            break
                    dropdown_active = False
                    if clicked_option:
                        continue

                # لو حد داس على القائمة عشان يفتحها
                if dropdown_rect.collidepoint(m_pos):
                    dropdown_active = True
                    continue

                # لو حد داس على اي زرار من خوارزميات البحث
                for btn in algo_buttons:
                    if btn["rect"].collidepoint(m_pos):
                        c_visited, c_path, c_stats = None, None, None
                        START, GOAL = (0, 0), (ROWS - 1, COLS - 1)

                        start_time = time.time()
                        path, visited = [], []

                        if btn["id"] == "BFS":
                            path, visited = bfs.run_bfs(MAZE, START, GOAL)
                        elif btn["id"] == "DFS":
                            path, visited = dfs.run_dfs(MAZE, START, GOAL)
                        elif btn["id"] == "UCS":
                            path, visited = ucs.run_ucs(MAZE, START, GOAL)
                        elif btn["id"] == "A* Manhattan":
                            path, visited, _ = a_star.a_star(
                                MAZE, START, GOAL, a_star.manhattan
                            )
                        elif btn["id"] == "A* Euclidean":
                            path, visited, _ = a_star.a_star(
                                MAZE, START, GOAL, a_star.euclidean
                            )

                        algo_time = time.time() - start_time
                        c_stats = animate_solution(visited, path, algo_time, c_stats)
                        c_visited, c_path = visited, path
                        msg = f"{btn['id']} Completed."

                # لو حد داس ريست
                if reset_btn["rect"].collidepoint(m_pos):
                    c_visited, c_path, c_stats = None, None, None
                    msg = "Environment Reset."

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
