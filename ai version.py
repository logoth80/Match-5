import tkinter as tk
import time


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
        if self.current_player == 1:
            row = event.y // 30
            col = event.x // 30

            if self.board[row][col] == 0:
                self.place_marker(row, col)
                if self.check_winner():
                    self.show_winner()
                else:
                    self.switch_player()
                    self.computer_move()

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
        winner = "Player 1" if self.current_player == 2 else "Player 2"
        tk.messagebox.showinfo("Game Over", f"{winner} wins!")
        self.root.quit()

    def computer_move(self):
        start_time = time.time()
        best_score = float("-inf")
        best_move = None

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    self.place_marker(row, col)
                    score = self.minimax(0, False, start_time + 1)
                    self.undo_move(row, col)

                    if time.time() > start_time + 1:
                        break

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

    def minimax(self, depth, is_maximizing, time_limit):
        if time.time() > time_limit:
            return 0

        if self.check_winner():
            return 10 - depth if self.current_player == 2 else depth - 10

        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = float("-inf")

            for row in range(self.size):
                for col in range(self.size):
                    if self.board[row][col] == 0:
                        self.place_marker(row, col)
                        score = self.minimax(depth + 1, False, time_limit)
                        self.undo_move(row, col)

                        best_score = max(score, best_score)

            return best_score
        else:
            best_score = float("inf")

            for row in range(self.size):
                for col in range(self.size):
                    if self.board[row][col] == 0:
                        self.place_marker(row, col)
                        score = self.minimax(depth + 1, True, time_limit)
                        self.undo_move(row, col)

                        best_score = min(score, best_score)

            return best_score

    def is_draw(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    return False
        return True

    def undo_move(self, row, col):
        self.board[row][col] = 0


if __name__ == "__main__":
    root = tk.Tk()
    game = MatchFiveGame(root)
    root.mainloop()
