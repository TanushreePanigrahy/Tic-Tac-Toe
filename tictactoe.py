from tkinter import *
import numpy as np 
size_of_board = 400
symbol_size = (size_of_board/3 - size_of_board/8) /2
symbol_thickness = 50
color_X = '#E81D1D'
color_O = '#2163EB'
color_score = '#3DB358'
color_tie = '#AFAF9D'
color_bg = '#E9C88D'

#GAME
class TicTacToe:
    def __init__(self):
        self.window = Tk()
        self.window.title("Tic Tac Toe")
        
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind("<Button-1>", self.click)
        self.draw_grid()
        
        self.board = np.zeros((3, 3))
        self.turn_X = True
        self.reset_ready = False
        self.score_X = 0
        self.score_O = 0
        self.score_tie = 0
    
    def draw_grid(self):
        # Draw 2 vertical and 2 horizontal lines
        for i in range(1, 3):
            self.canvas.create_line(i * size_of_board / 3, 0, i * size_of_board / 3, size_of_board)
            self.canvas.create_line(0, i * size_of_board / 3, size_of_board, i * size_of_board / 3)

    def draw_X(self, pos):
        cx, cy = self.get_center(pos)
        d = symbol_size
        self.canvas.create_line(cx - d, cy - d, cx + d, cy + d, width=symbol_thickness, fill=color_X)
        self.canvas.create_line(cx - d, cy + d, cx + d, cy - d, width=symbol_thickness, fill=color_X)

    def draw_O(self, pos):
        cx, cy = self.get_center(pos)
        d = symbol_size
        self.canvas.create_oval(cx - d, cy - d, cx + d, cy + d, width=symbol_thickness, outline=color_O)

    def get_center(self, pos):
        return (pos[1] * size_of_board / 3 + size_of_board / 6, pos[0] * size_of_board / 3 + size_of_board / 6)

    def grid_from_click(self, x, y):
        return int(y // (size_of_board / 3)), int(x // (size_of_board / 3))

    def is_winner(self, player_val):
        b = self.board
        for i in range(3):
            if all(b[i, :] == player_val) or all(b[:, i] == player_val):
                return True
        if b[0, 0] == b[1, 1] == b[2, 2] == player_val or b[0, 2] == b[1, 1] == b[2, 0] == player_val:
            return True
        return False

    def is_tie(self):
        return np.all(self.board != 0)

    def click(self, event):
        if self.reset_ready:
            self.reset_game()
            return

        row, col = self.grid_from_click(event.x, event.y)

        if self.board[row][col] != 0:
            return  # Spot already taken

        if self.turn_X:
            self.draw_X((row, col))
            self.board[row][col] = -1
        else:
            self.draw_O((row, col))
            self.board[row][col] = 1

        self.turn_X = not self.turn_X  # Switch turn

        if self.is_winner(-1):
            self.score_X += 1
            self.show_result("Player X Wins!", color_X)
        elif self.is_winner(1):
            self.score_O += 1
            self.show_result("Player O Wins!", color_O)
        elif self.is_tie():
            self.score_tie += 1
            self.show_result("It's a Tie!", color_tie)

    def show_result(self, message, color):
        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, text=message, font="Helvetica 40 bold", fill=color)

        score_text = f"Score\nX: {self.score_X}  O: {self.score_O}  Ties: {self.score_tie}"
        self.canvas.create_text(size_of_board / 2, size_of_board / 2, text=score_text, font="Helvetica 24 bold", fill=color_score)

        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 6, text="Click anywhere to play again",
                                font="Helvetica 16 italic", fill="gray")

        self.reset_ready = True

    def reset_game(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.board = np.zeros((3, 3))
        self.turn_X = True
        self.reset_ready = False

    def run(self):
        self.window.mainloop()


# Start Game
if __name__ == "__main__":
    game = TicTacToe()
    game.run()