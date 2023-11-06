import pygame
import random
from collections import defaultdict
import time
import sqlite3

def game(user_choice, username):
    pygame.init()

    player_num = user_choice['num_players']

    difficulty = user_choice['difficulty']
    if difficulty == "Easy":
        CELL_SIZE = 50
    elif difficulty == "Medium":
        CELL_SIZE = 40
    elif difficulty == "Hard":
        CELL_SIZE = 30

    # Constants
    WIDTH, HEIGHT = 600, 600
    PADDING = CELL_SIZE // 4
    ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Maze Game')


    class Cell:
        def __init__(self, row, col):
            self.row = row
            self.col = col
            self.edges = []
            self.visited = False

        def pos(self):
            return (self.row, self.col)

        def get_neighbors(self, grid):
            neighbors = []
            if self.row > 0:  # top neighbor
                neighbors.append(grid[self.row - 1][self.col])
            if self.row < ROWS - 1:  # bottom neighbor
                neighbors.append(grid[self.row + 1][self.col])
            if self.col > 0:  # left neighbor
                neighbors.append(grid[self.row][self.col - 1])
            if self.col < COLS - 1:  # right neighbor
                neighbors.append(grid[self.row][self.col + 1])
            return neighbors

    class Player:
        def __init__(self, x, y, color):
            self.x = x
            self.y = y
            self.color = color

        def draw(self, screen):
            pygame.draw.rect(screen, self.color, (self.x, self.y, CELL_SIZE - PADDING, CELL_SIZE - PADDING))

    # Define a list of starting positions for players
    starting_positions = [(0, 0), (0, CELL_SIZE), (CELL_SIZE, 0)]

    starting_positions = starting_positions[:player_num]

    # Define players with different colors for distinction
    colors = []
    for color in user_choice['players']:
        if color == "Red":
            colors.append((255, 0, 0))
        elif color == "Green":
            colors.append((0, 255, 0))
        elif color == "Blue":
            colors.append((0, 0, 255))
        elif color == "Black":
            colors.append((0, 0, 0))
    colors = colors[:player_num]
    players = [Player(pos[0], pos[1], color) for pos, color in zip(starting_positions, colors)]

    # Define player controls
    player_controls = [
        {pygame.K_UP: (0, -CELL_SIZE), pygame.K_DOWN: (0, CELL_SIZE), pygame.K_LEFT: (-CELL_SIZE, 0), pygame.K_RIGHT: (CELL_SIZE, 0)},  # Arrow keys
        {pygame.K_w: (0, -CELL_SIZE), pygame.K_s: (0, CELL_SIZE), pygame.K_a: (-CELL_SIZE, 0), pygame.K_d: (CELL_SIZE, 0)},  # WASD
        {pygame.K_i: (0, -CELL_SIZE), pygame.K_k: (0, CELL_SIZE), pygame.K_j: (-CELL_SIZE, 0), pygame.K_l: (CELL_SIZE, 0)}   # IJKL
    ]
    player_controls = player_controls[:player_num]

    def valid_move(mst, x, y, current_x, current_y):
        # Check if the new position is within screen bounds
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return False

        # Determine the current cell and the direction of the move
        curr_cell = (current_y // CELL_SIZE, current_x // CELL_SIZE)
        next_cell = (y // CELL_SIZE, x // CELL_SIZE)

        # Check if the move is valid
        if next_cell not in mst.get(curr_cell, []):
            return False

        # All checks passed
        return True

    def make_edges(grid):
        edges = defaultdict(list)

        for row in grid:
            for cell in row:
                neighbors = cell.get_neighbors(grid)
                for neighbor in neighbors:
                    weight = random.randint(1, 100)
                    edge = (cell.pos(), neighbor.pos())
                    edges[edge] = weight

        return edges

    def find(cell, parent):
        if parent[cell] != cell:
            parent[cell] = find(parent[cell], parent)
        return parent[cell]

    def union(cell1, cell2, parent, rank):
        root1 = find(cell1, parent)
        root2 = find(cell2, parent)

        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            else:
                parent[root1] = root2
                if rank[root1] == rank[root2]: rank[root2] += 1

    def kruskal(grid, edges):
        forest = defaultdict(list)
        parent = {}
        rank = defaultdict(int)

        for row in grid:
            for cell in row:
                parent[cell.pos()] = cell.pos()

        for edge, weight in sorted(edges.items(), key=lambda item: item[1]):
            cell1, cell2 = edge
            if find(cell1, parent) != find(cell2, parent):
                forest[cell1].append(cell2)
                forest[cell2].append(cell1)
                union(cell1, cell2, parent, rank)

        return forest

    def draw_maze(grid, mst, player):
        screen.fill(WHITE)

        for row in grid:
            for cell in row:
                x, y = cell.col * CELL_SIZE, cell.row * CELL_SIZE
                neighbors = mst.get(cell.pos(), [])

                if not ((cell.row, cell.col - 1) in neighbors):  # left
                    pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE))
                if not ((cell.row - 1, cell.col) in neighbors):  # top
                    pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y))
                if not ((cell.row, cell.col + 1) in neighbors):  # right
                    pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE))
                if not ((cell.row + 1, cell.col) in neighbors):  # bottom
                    pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE))

        padding = CELL_SIZE // 10
        pygame.draw.rect(screen, GREEN, (0, 0, CELL_SIZE, CELL_SIZE))
        finish_square_rect = pygame.Rect(WIDTH - CELL_SIZE + padding, HEIGHT - CELL_SIZE + padding, CELL_SIZE - (2 * padding), CELL_SIZE - (2 * padding))

        pygame.draw.rect(screen, (64, 224, 208), (WIDTH - CELL_SIZE + padding, HEIGHT - CELL_SIZE + padding, CELL_SIZE - (2 * padding), CELL_SIZE - (2 * padding)))
        # Draw the "FINISH" text on the square
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', CELL_SIZE // 5)
        text_surface = myfont.render('FINISH', False, (0, 0, 0))
        text_rect = text_surface.get_rect(center=finish_square_rect.center)  # This centers the text in the rectangle
        screen.blit(text_surface, text_rect.topleft)
        pygame.display.flip()
        for player in players:
            player.draw(screen)  # Draw each player on the screen

        pygame.display.flip()

    def draw_player(screen, player, old_pos, mst):
        old_x, old_y = old_pos
        x, y = player.x, player.y

        # Clear the old position by redrawing that part of the maze
        pygame.draw.rect(screen, WHITE, (old_x, old_y, CELL_SIZE, CELL_SIZE))

        neighbors = mst.get((old_y // CELL_SIZE, old_x // CELL_SIZE), [])

        if not ((old_y // CELL_SIZE, old_x // CELL_SIZE - 1) in neighbors):  # left
            pygame.draw.line(screen, BLACK, (old_x, old_y), (old_x, old_y + CELL_SIZE))
        if not ((old_y // CELL_SIZE - 1, old_x // CELL_SIZE) in neighbors):  # top
            pygame.draw.line(screen, BLACK, (old_x, old_y), (old_x + CELL_SIZE, old_y))
        if not ((old_y // CELL_SIZE, old_x // CELL_SIZE + 1) in neighbors):  # right
            pygame.draw.line(screen, BLACK, (old_x + CELL_SIZE, old_y), (old_x + CELL_SIZE, old_y + CELL_SIZE))
        if not ((old_y // CELL_SIZE + 1, old_x // CELL_SIZE) in neighbors):  # bottom
            pygame.draw.line(screen, BLACK, (old_x, old_y + CELL_SIZE), (old_x + CELL_SIZE, old_y + CELL_SIZE))

        # Now, draw the player at the new position
        padding = CELL_SIZE // 10
        pygame.draw.rect(screen, player.color, (x + padding, y + padding, CELL_SIZE - 2 * padding, CELL_SIZE - 2 * padding))

        # Refresh only the part of the screen where the player moved
        pygame.display.update((old_x, old_y, CELL_SIZE, CELL_SIZE))
        pygame.display.update((x, y, CELL_SIZE, CELL_SIZE))

    def display_message(screen, player_scores, score_type=None):
        # Headings
        headings = ["Ranking", "Player", "Score"]

        # Compute font size as a fraction (e.g., 1/20th) of the smaller maze dimension
        font_size = min(WIDTH, HEIGHT) // 20
        font = pygame.font.SysFont(None, font_size)

        screen.fill(WHITE)  # Clear the screen

        # Only add the header if the score_type is specified
        if score_type:
            if score_type == "local":
                header_message = f"Local High Scores for {difficulty} level"
            else:
                header_message = f"Global High Scores for {difficulty} level"

            header_surface = font.render(header_message, True, (0, 0, 0))
            header_rect = header_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))  # Adjust vertical positioning
            screen.blit(header_surface, header_rect)

        # Adjust the starting_y based on the presence of the header
        starting_y = HEIGHT // 4 if score_type else HEIGHT // 2

        # Display the list of scores
        if isinstance(player_scores, list):
            for i, (name, score) in enumerate(player_scores, start=1):  # start=1 for ranking from 1

                rank_str = "{}.".format(i)
                rank_surface = font.render(rank_str, True, (0, 0, 0))
                rank_rect = rank_surface.get_rect(topleft=(WIDTH * 0.25, starting_y + i * font_size))
                screen.blit(rank_surface, rank_rect)

                name_str = name
                name_surface = font.render(name_str, True, (0, 0, 0))

                # Adjust the centery of the name to match the rank's centery
                name_rect = name_surface.get_rect(center=(WIDTH // 2, rank_rect.centery))
                screen.blit(name_surface, name_rect)

                score_str = str(score)
                score_surface = font.render(score_str, True, (0, 0, 0))

                # Adjust the centery of the score to match the rank's and name's centery
                score_rect = score_surface.get_rect(center=(WIDTH * 0.75, rank_rect.centery))
                screen.blit(score_surface, score_rect)

        # Display a single message (e.g., winner announcement, play again?)
        else:
            text_surface = font.render(player_scores, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_surface, text_rect)

        pygame.display.update()

    def draw_players(screen, players, old_positions, mst):
        for i, player in enumerate(players):
            draw_player(screen, player, old_positions[i], mst)

    def store_winner_score(account, player_name, score, difficulty):

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Insert the player's score into the all_scores table
        query = 'INSERT INTO scores (account, name, score, difficulty) VALUES (?, ?, ?, ?);'

        cursor.execute(query, (account, player_name, score, difficulty))
        conn.commit()  # Save the changes
        conn.close()

    def get_local_high_scores(account, difficulty):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        query = '''SELECT name, MIN(score) as min_score
                   FROM scores 
                   WHERE account = ? and difficulty = ?
                   GROUP BY name
                   ORDER BY min_score
                   LIMIT 10;'''

        cursor.execute(query, (account, difficulty))
        scores = cursor.fetchall()
        conn.close()

        return scores

    def get_global_high_scores(difficulty):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        query = '''SELECT name, MIN(score) as min_score
                           FROM scores 
                           WHERE difficulty = ?
                           GROUP BY name
                           ORDER BY min_score
                           LIMIT 10;'''

        cursor.execute(query, (difficulty,))
        scores = cursor.fetchall()
        conn.close()

        return scores

    def wait_for_click():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return

    def display_timer(screen, time_remaining):
        font_size = min(WIDTH, HEIGHT) // 20
        font = pygame.font.SysFont(None, font_size)
        timer_text = "{:02d}:{:02d}".format(time_remaining // 60, time_remaining % 60)
        timer_surface = font.render(timer_text, True, (0, 0, 0))
        timer_rect = timer_surface.get_rect(topright=(WIDTH - 10, 10))

        # Clear the old timer text
        clear_rect = pygame.Rect(0.85 * WIDTH, 2, 0.15 * WIDTH, font_size)  # Adjust as needed
        pygame.draw.rect(screen, WHITE, clear_rect)

        screen.blit(timer_surface, timer_rect)
        pygame.display.update(clear_rect)  # Update the entire timer area

    time_limits = {
        'Easy': 60,  # 1 minute
        'Medium': 180,  # 3 minutes
        'Hard': 300  # 5 minutes
    }
    def main():
        while True:
            grid = [[Cell(row, col) for col in range(COLS)] for row in range(ROWS)]
            edges = make_edges(grid)
            mst = kruskal(grid, edges)

            # Initialize players, controls, and old_positions
            starting_positions = [(0, 0), (0, CELL_SIZE), (CELL_SIZE, 0)][:player_num]
            colors = []
            for player in user_choice['players']:
                if player['color'] == "Red":
                    colors.append((255, 0, 0))
                elif player['color'] == "Green":
                    colors.append((0, 255, 0))
                elif player['color'] == "Blue":
                    colors.append((0, 0, 255))
                elif player['color'] == "Black":
                    colors.append((0, 0, 0))
            colors = colors[:player_num]
            players = [Player(pos[0], pos[1], color) for pos, color in zip(starting_positions, colors)]
            old_positions = starting_positions.copy()

            # Assuming the end is bottom-right
            end_pos = (WIDTH - CELL_SIZE, HEIGHT - CELL_SIZE)

            start_time = time.time()
            time_limit = time_limits[difficulty]
            # Draw the maze with all players at the start
            draw_maze(grid, mst, players)

            running = True
            while running:
                current_time = time.time()
                elapsed_time = current_time - start_time
                time_remaining = max(time_limit - elapsed_time, 0)
                if time_remaining <= 0:
                    # 4. Handle Time Running Out
                    print("Time's Up!")
                    display_message(screen, 'Time\'s Up! You Lost.')
                    wait_for_click()  # Waiting for user click to proceed
                    display_message(screen, 'Return to Home? (Y/N)')

                    waiting_for_decision = True
                    while waiting_for_decision:
                        for evt in pygame.event.get():
                            if evt.type == pygame.KEYDOWN:
                                if evt.key == pygame.K_y:
                                    pygame.quit()
                                    return True
                                if evt.key in [pygame.K_n, pygame.K_ESCAPE]:
                                    running = False
                                    waiting_for_decision = False

                    display_message(screen, 'Play again? (Y/N)')

                    waiting_for_decision = True
                    while waiting_for_decision:
                        for evt in pygame.event.get():
                            if evt.type == pygame.KEYDOWN:
                                if evt.key == pygame.K_y:
                                    running = False
                                    waiting_for_decision = False
                                if evt.key in [pygame.K_n, pygame.K_ESCAPE]:
                                    pygame.quit()
                                    return False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        for i, player in enumerate(players):
                            if event.key in player_controls[i]:
                                dx, dy = player_controls[i][event.key]
                                next_x = player.x + dx
                                next_y = player.y + dy
                                if valid_move(mst, next_x, next_y, player.x, player.y):
                                    old_positions[i] = (player.x, player.y)
                                    player.x = next_x
                                    player.y = next_y

                    draw_players(screen, players, old_positions, mst)

                display_timer(screen, int(time_remaining))
                # Check for winning condition
                for i, player in enumerate(players):
                    if player.x == end_pos[0] and player.y == end_pos[1]:
                        elapsed_time = round(time.time() - start_time, 2)
                        player_name = user_choice['players'][i]['name']
                        display_message(screen, f'{player_name} Wins! Time taken: {elapsed_time} seconds.')
                        wait_for_click()  # Waiting for user click to proceed
                        store_winner_score(username, player_name, elapsed_time, difficulty)

                        # Add function to inform the user if the local or global high score has been beaten
                        local_scores = get_local_high_scores(username, difficulty)
                        global_scores = get_global_high_scores(difficulty)
                        print(local_scores)
                        if elapsed_time == global_scores[0][1]:
                            display_message(screen, f"Global high score beaten by {player_name}!")
                            wait_for_click()  # Waiting for user click to proceed
                        elif elapsed_time == local_scores[0][1]:
                            display_message(screen, f"Local high score beaten by {player_name}!")
                            wait_for_click()  # Waiting for user click to proceed


                        display_message(screen, local_scores, "local")
                        wait_for_click()  # Waiting for user click to proceed

                        display_message(screen, global_scores, "global")
                        wait_for_click()  # Waiting for user click to proceed

                        display_message(screen, 'Return to Home? (Y/N)')

                        waiting_for_decision = True
                        while waiting_for_decision:
                            for evt in pygame.event.get():
                                if evt.type == pygame.KEYDOWN:
                                    if evt.key == pygame.K_y:
                                        pygame.quit()
                                        return True
                                    if evt.key in [pygame.K_n, pygame.K_ESCAPE]:
                                        running = False
                                        waiting_for_decision = False

                        display_message(screen, 'Play again? (Y/N)')

                        waiting_for_decision = True
                        while waiting_for_decision:
                            for evt in pygame.event.get():
                                if evt.type == pygame.KEYDOWN:
                                    if evt.key == pygame.K_y:
                                        running = False
                                        waiting_for_decision = False
                                    if evt.key in [pygame.K_n, pygame.K_ESCAPE]:
                                        pygame.quit()
                                        return False

    home = main()
    return home

if __name__ == "__main__":
    choice = {'difficulty': 'Easy', 'num_players': 3, 'players': [{'name': 'Shahu', 'color': 'Red'}, {'name': 'Sam', 'color': 'Green'}, {'name': 'John', 'color': 'Blue'}]}
    result = game(choice, 'test')
    print(result)