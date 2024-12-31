import tkinter as tk
import pygame
import random


class MatchFiveGame:
    pygame.init()
    global sounds_o
    global sounds_x
    sounds_o = ["marker o1.mp3", "marker o2.mp3"]
    sounds_x = ["marker x1.mp3", "marker x2.mp3", "marker x3.mp3"]

    global box_size
    box_size = 45
    global grid_xy
    grid_xy = 25

    def __init__(self, root):
        self.root = root
        self.root.title("Match Five Game")

        self.size = grid_xy
        self.board = [[0] * self.size for _ in range(self.size)]
        self.current_player = 1

        self.canvas = tk.Canvas(
            root,
            width=self.size * box_size,
            height=self.size * box_size,
            bg="white",
        )
        self.canvas.pack()
        self.draw_board()
        self.center_window()
        self.canvas.bind("<Button-1>", self.on_click)

        # Add a toggle button
        self.toggle_button = tk.Button(root, text="Player vs Computer", command=self.toggle_mode)
        self.toggle_button.pack(side=tk.BOTTOM)

    def toggle_mode(self):
        if self.toggle_button["text"] == "Player vs Computer":
            self.toggle_button.config(text="Player vs Player")
            # self.current_player = 1  # Reset to player 1 for new game
        else:
            self.toggle_button.config(text="Player vs Computer")
            if self.current_player == 2:  # Switch to player 2 for new game
                self.ai_move()

    def center_window(self):
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{self.size * box_size}x{self.size * box_size+30}+{x}+{y}")

    def draw_board(self):
        for i in range(1, self.size):
            self.canvas.create_line(i * box_size, 0, i * box_size, self.size * box_size, fill="powder blue")
            self.canvas.create_line(0, i * box_size, self.size * box_size, i * box_size, fill="powder blue")

    def on_click(self, event):
        if self.current_player == 1 or (self.toggle_button["text"] == "Player vs Player"):  # Human player's turn
            row = event.y // box_size
            col = event.x // box_size

            if self.board[row][col] == 0:
                self.place_marker(row, col)
                if self.check_possible_winner():
                    self.show_winner()
                else:
                    if self.toggle_button["text"] == "Player vs Computer":
                        self.switch_player()
                        self.root.after(100, self.ai_move)
                    else:
                        self.switch_player()

    def place_marker(self, row, col):
        self.board[row][col] = self.current_player
        x1, y1 = col * box_size + 5, row * box_size + 5
        x2, y2 = (col + 1) * box_size - 5, (row + 1) * box_size - 5

        if self.current_player == 1:
            select_sound = random.choice(sounds_o)
            self.canvas.create_oval(x1, y1, x2, y2, outline="black", width="3")
            pygame.mixer.music.load(select_sound)
            pygame.mixer.music.play()
        else:
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=3)
            self.canvas.create_line(x1, y2, x2, y1, fill="blue", width=3)
            select_sound = random.choice(sounds_x)
            pygame.mixer.music.load(select_sound)
            pygame.mixer.music.play()

    def switch_player(self):
        self.current_player = 3 - self.current_player

    def cross_winner(self):
        directions = [
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
        ]

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != 0:
                    player = self.board[row][col]
                    winning_sequence = []
                    winning_sequence.append((col, row))

                    for dx, dy in directions:
                        count = 1

                        x, y = row + dx, col + dy
                        while 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == player:
                            count += 1
                            winning_sequence.append((y, x))
                            x += dx
                            y += dy

                        if count >= 5:
                            offsetbox = box_size // 2
                            for step in range(0, winning_sequence.__len__() - 1):
                                self.canvas.create_line(
                                    (
                                        winning_sequence[step][0] * box_size + offsetbox,
                                        winning_sequence[step][1] * box_size + offsetbox,
                                    ),
                                    (
                                        winning_sequence[step + 1][0] * box_size + offsetbox,
                                        winning_sequence[step + 1][1] * box_size + offsetbox,
                                    ),
                                    width=box_size // 6,
                                    fill="red",
                                )
                            return

    def check_possible_winner(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != 0:
                    player = self.board[row][col]
                    for dx, dy in directions:
                        count = 1

                        # Check forward
                        x, y = row + dx, col + dy
                        while 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == player:
                            count += 1
                            x += dx
                            y += dy

                        # Check backward
                        x, y = row - dx, col - dy
                        while 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == player:
                            count += 1
                            x -= dx
                            y -= dy
                        if count >= 5:
                            return True
        return False

    def check_possible_four(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != 0:
                    player = self.board[row][col]
                    for dx, dy in directions:
                        count = 1
                        open_ends = 0

                        # Check forward
                        x, y = row + dx, col + dy
                        while 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == player:
                            count += 1
                            x += dx
                            y += dy
                        if 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == 0:
                            open_ends += 1
                        # Check backward
                        x, y = row - dx, col - dy
                        while 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == player:
                            count += 1
                            x -= dx
                            y -= dy
                        if 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == 0:
                            open_ends += 1
                        if count >= 4 and open_ends > 0:
                            print(f"possible 4 at {row}, {col}")
                            # return True

        return False

    def show_winner(self):
        self.cross_winner()
        winner = "Player 1" if self.current_player == 1 else "Player 2"
        tk.messagebox.showinfo("Game Over", f"{winner} wins!")
        root.destroy()

    def ai_move(self):
        if self.current_player != 2:  # Only AI moves in Player vs Computer mode
            return

        best_move = None
        best_score = -float("inf")
        block_priority = None

        if not any(2 in row for row in self.board):  # First AI move logic
            # Prioritize moving closer to the center
            center = self.size // 2
            for dx, dy in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                potential_row, potential_col = center + dx, center + dy
                if 0 <= potential_row < self.size and 0 <= potential_col < self.size and self.board[potential_row][potential_col] == 0:
                    self.place_marker(potential_row, potential_col)
                    self.switch_player()
                    return

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    # AI checks if it can win
                    self.board[row][col] = 2
                    if self.check_possible_winner():
                        self.board[row][col] = 0
                        self.place_marker(row, col)
                        self.show_winner()
                        return
                    self.board[row][col] = 0

                    # AI checks if it must block Player 1's win
                    self.board[row][col] = 1
                    if self.check_possible_winner():
                        self.board[row][col] = 0
                        block_priority = (row, col)
                    self.board[row][col] = 0

        if block_priority:
            row, col = block_priority
            self.place_marker(row, col)
            self.switch_player()
            return

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    self.board[row][col] = 2
                    score = self.evaluate_board(2) - self.evaluate_board(1)
                    self.board[row][col] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        if best_move:
            row, col = best_move
            self.place_marker(row, col)
            if self.check_possible_winner():
                self.show_winner()
            else:
                self.switch_player()

    def evaluate_board(self, player):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == player:
                    for dx, dy in directions:
                        count = 1
                        open_ends = 0

                        # Check forward
                        x, y = row + dx, col + dy
                        while 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == player:
                            count += 1
                            x += dx
                            y += dy
                        if 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == 0:
                            open_ends += 1

                        # Check backward
                        x, y = row - dx, col - dy
                        while 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == player:
                            count += 1
                            x -= dx
                            y -= dy
                        if 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == 0:
                            open_ends += 1

                        if count == 3 and open_ends == 2:
                            score += 1000  # High priority to block or extend 3 with open ends
                        elif count == 1:
                            score += 20
                        elif count == 2 and open_ends == 2:
                            score += 40
                        elif count == 2:
                            score += 35
                        elif count == 3:
                            score += 80
                        elif count == 4 and open_ends == 2:
                            score += 5000
                        elif count == 4 and open_ends == 1:
                            score += 200
                        if count + self.remaining_space(row, col, dx, dy) < 5:
                            score -= 100
        return score

    def remaining_space(self, row, col, dx, dy):
        space = 0

        # Check forward
        x, y = row + dx, col + dy
        while 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == 0:
            space += 1
            x += dx
            y += dy

        # Check backward
        x, y = row - dx, col - dy
        while 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == 0:
            space += 1
            x -= dx
            y -= dy

        return space


if __name__ == "__main__":

    def on_closing():
        global restarting_loop
        restarting_loop = False
        root.destroy()

    def key_handler(event):
        print(str(event.keycode))
        if event.keycode == 27:
            global restarting_loop
            restarting_loop = False
            root.destroy()
        if event.keycode == 116:
            root.destroy()
        return

    restarting_loop = True

    while restarting_loop:
        root = tk.Tk()
        game = MatchFiveGame(root)
        root.bind("<Key>", key_handler)
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
