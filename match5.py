import tkinter as tk
from tkinter import messagebox


class MatchFiveGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Match Five Game")

        self.size = 25
        self.board = [[0] * self.size for _ in range(self.size)]
        self.current_player = 1

        self.canvas = tk.Canvas(root, width=self.size * 30, height=self.size * 30)
        self.canvas.pack()

        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        for i in range(1, self.size):
            self.canvas.create_line(i * 30, 0, i * 30, self.size * 30)
            self.canvas.create_line(0, i * 30, self.size * 30, i * 30)

    def on_click(self, event):
        if self.current_player == 1:  # Human player's turn
            row = event.y // 30
            col = event.x // 30

            if self.board[row][col] == 0:
                self.place_marker(row, col)
                if self.check_winner():
                    self.show_winner()
                else:
                    self.switch_player()
                    self.ai_move()  # Trigger AI move after Player 1

    def place_marker(self, row, col):
        self.board[row][col] = self.current_player
        x1, y1 = col * 30 + 5, row * 30 + 5
        x2, y2 = (col + 1) * 30 - 5, (row + 1) * 30 - 5

        if self.current_player == 1:
            self.canvas.create_oval(x1, y1, x2, y2, fill="red")
        else:
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=5)

    def switch_player(self):
        self.current_player = 3 - self.current_player

    def check_winner(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != 0:
                    player = self.board[row][col]

                    for dx, dy in directions:
                        count = 1

                        # Check forward
                        x, y = row + dx, col + dy
                        while (
                            0 <= x < self.size
                            and 0 <= y < self.size
                            and self.board[x][y] == player
                        ):
                            count += 1
                            x += dx
                            y += dy

                        # Check backward
                        x, y = row - dx, col - dy
                        while (
                            0 <= x < self.size
                            and 0 <= y < self.size
                            and self.board[x][y] == player
                        ):
                            count += 1
                            x -= dx
                            y -= dy

                        if count >= 5:
                            return True

        return False

    def show_winner(self):
        winner = "Player 1" if self.current_player == 1 else "Player 2"
        tk.messagebox.showinfo("Game Over", f"{winner} wins!")
        self.root.quit()

    def ai_move(self):
        best_move = None
        best_score = -float("inf")
        block_priority = None

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    # AI checks if it can win
                    self.board[row][col] = 2
                    if self.check_winner():
                        self.board[row][col] = 0
                        self.place_marker(row, col)
                        self.show_winner()
                        return
                    self.board[row][col] = 0

                    # AI checks if it must block Player 1's win
                    self.board[row][col] = 1
                    if self.check_winner():
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
            if self.check_winner():
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
                        while (
                            0 <= x < self.size
                            and 0 <= y < self.size
                            and self.board[x][y] == player
                        ):
                            count += 1
                            x += dx
                            y += dy
                        if (
                            0 <= x < self.size
                            and 0 <= y < self.size
                            and self.board[x][y] == 0
                        ):
                            open_ends += 1

                        # Check backward
                        x, y = row - dx, col - dy
                        while (
                            0 <= x < self.size
                            and 0 <= y < self.size
                            and self.board[x][y] == player
                        ):
                            count += 1
                            x -= dx
                            y -= dy
                        if (
                            0 <= x < self.size
                            and 0 <= y < self.size
                            and self.board[x][y] == 0
                        ):
                            open_ends += 1

                        if count == 3 and open_ends == 2:
                            score += 1000  # High priority to block or extend 3 with open ends
                        elif count == 1 and open_ends == 2:
                            score += 20
                        elif count == 2 and open_ends == 2:
                            score += 40
                        elif count == 2:
                            score += 35
                        elif count == 3:
                            score += 60
                        elif count == 4:
                            score += 500

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
    root = tk.Tk()
    game = MatchFiveGame(root)
    root.mainloop()
