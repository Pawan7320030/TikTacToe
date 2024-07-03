import tkinter as tk
from tkinter import ttk, messagebox
import time

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10)

        self.instruction_frame = tk.Frame(self.notebook, bg="white")
        self.player_frame = tk.Frame(self.notebook, bg="white")
        self.game_frame = tk.Frame(self.notebook)

        self.notebook.add(self.instruction_frame, text="Instructions")
        self.notebook.add(self.player_frame, text="Player Selection")
        self.notebook.add(self.game_frame, text="Game")

        self.create_instruction_page()
        self.create_player_selection_page()
        self.create_game_page()

        self.current_player = "X"  # Player X starts first
        self.moves = [[" " for _ in range(3)] for _ in range(3)]
        self.game_over = False

    def create_instruction_page(self):
        label = tk.Label(self.instruction_frame, text="Instructions:", font=("Arial", 16), bg="white")
        label.pack(pady=20)

        instructions_text = """
        Welcome to Tic Tac Toe!
        
        - Click on any box to start the game.
        - Toggle the color of the box with each click.
        - Restart button resets the game.
        - Enjoy playing!
        """
        instructions_label = tk.Label(self.instruction_frame, text=instructions_text, justify=tk.LEFT, bg="white")
        instructions_label.pack(padx=20, pady=10)

    def create_player_selection_page(self):
        label = tk.Label(self.player_frame, text="Player Selection:", font=("Arial", 16), bg="white")
        label.pack(pady=20)

        # Add player selection widgets if needed

        start_button = tk.Button(self.player_frame, text="Start Game", command=self.show_game_page)
        start_button.pack(pady=10)

    def create_game_page(self):
        self.game_frame.rowconfigure(0, weight=1)
        self.game_frame.columnconfigure(0, weight=1)

        self.instructions_label = tk.Label(self.game_frame, text="Click on any box to start!", font=("Arial", 12))
        self.instructions_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.restart_button = tk.Button(self.game_frame, text="Restart", command=self.restart_game)
        self.restart_button.grid(row=4, column=1, columnspan=1, padx=10, pady=10)

        self.timer_label = tk.Label(self.game_frame, text="Time Elapsed: 0 seconds", font=("Arial", 10))
        self.timer_label.grid(row=5, column=0, columnspan=3)

        self.buttons = []
        self.current_color = "#FFFFFF"
        self.start_time = None

        # Create 3x3 grid of buttons
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.game_frame, text=" ", width=10, height=5, bg=self.current_color, bd=4,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i+1, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)

    def on_button_click(self, row, col):
        if self.moves[row][col] == " " and not self.game_over:
            self.moves[row][col] = self.current_player
            self.buttons[row][col].configure(text=self.current_player)

            if self.check_winner():
                self.instructions_label.configure(text=f"Player {self.current_player} wins!")
                self.game_over = True
                messagebox.showinfo("Game Over", f"Congratulations, Player {self.current_player}!")
            elif self.check_draw():
                self.instructions_label.configure(text="It's a draw!")
                self.game_over = True

            if not self.game_over:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.instructions_label.configure(text=f"Player {self.current_player}'s turn")

                if self.start_time is None:
                    self.start_time = time.time()
                    self.update_timer()

    def check_winner(self):
        # Check rows
        for i in range(3):
            if self.moves[i][0] == self.moves[i][1] == self.moves[i][2] != " ":
                return True

        # Check columns
        for j in range(3):
            if self.moves[0][j] == self.moves[1][j] == self.moves[2][j] != " ":
                return True

        # Check diagonals
        if self.moves[0][0] == self.moves[1][1] == self.moves[2][2] != " ":
            return True
        if self.moves[0][2] == self.moves[1][1] == self.moves[2][0] != " ":
            return True

        return False

    def check_draw(self):
        for row in self.moves:
            for move in row:
                if move == " ":
                    return False
        return True

    def restart_game(self):
        self.moves = [[" " for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.current_player = "X"
        self.instructions_label.configure(text="Click on any box to start!")
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text=" ")

    def update_timer(self):
        if self.start_time is not None and not self.game_over:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.configure(text=f"Time Elapsed: {elapsed_time} seconds")
            self.root.after(1000, self.update_timer)

    def show_game_page(self):
        self.notebook.select(2)  # Switch to the game page

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
