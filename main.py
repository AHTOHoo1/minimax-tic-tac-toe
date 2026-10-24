
import tkinter as tk
from tkinter import messagebox

# ============================================================
# AI LABORATORY WORK 2
# Tic-Tac-Toe: Human vs AI
# Algorithm: Minimax
# ============================================================

BOARD_SIZE = 3

HUMAN = "X"
AI = "O"
EMPTY = ""

AI_WIN_SCORE = 10
HUMAN_WIN_SCORE = -10
DRAW_SCORE = 0

# Interface colors
BG_COLOR = "#10141F"
PANEL_COLOR = "#191F2E"
CELL_COLOR = "#222A3B"
CELL_HOVER = "#303B52"
TEXT_COLOR = "#F3F4F6"
MUTED_COLOR = "#9CA3AF"
X_COLOR = "#38BDF8"
O_COLOR = "#FBBF24"
ACCENT_COLOR = "#6366F1"
WIN_COLOR = "#34D399"


# ============================================================
# GAME LOGIC
# ============================================================

def create_board():
    """Create an empty 3x3 board."""
    return [[EMPTY for _ in range(BOARD_SIZE)]
            for _ in range(BOARD_SIZE)]


def get_available_moves(board):
    """Return all empty cells as (row, col)."""
    moves = []

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY:
                moves.append((row, col))

    return moves


def apply_move(board, move, player):
    """Place a symbol on the board."""
    row, col = move
    board[row][col] = player


def undo_move(board, move):
    """Undo a simulated move during Minimax."""
    row, col = move
    board[row][col] = EMPTY


def check_winner(board):
    """Return the winning symbol or None."""

    # Check rows
    for row in range(BOARD_SIZE):
        if (
            board[row][0] != EMPTY
            and board[row][0] == board[row][1] == board[row][2]
        ):
            return board[row][0]

    # Check columns
    for col in range(BOARD_SIZE):
        if (
            board[0][col] != EMPTY
            and board[0][col] == board[1][col] == board[2][col]
        ):
            return board[0][col]

    # Main diagonal
    if (
        board[0][0] != EMPTY
        and board[0][0] == board[1][1] == board[2][2]
    ):
        return board[0][0]

    # Opposite diagonal
    if (
        board[0][2] != EMPTY
        and board[0][2] == board[1][1] == board[2][0]
    ):
        return board[0][2]

    return None


def is_terminal(board):
    """Check whether the game has ended."""
    return (
        check_winner(board) is not None
        or len(get_available_moves(board)) == 0
    )


def evaluate(board):
    """
    Evaluate terminal states:
    AI win    = +10
    Human win = -10
    Draw      = 0
    """
    winner = check_winner(board)

    if winner == AI:
        return AI_WIN_SCORE

    if winner == HUMAN:
        return HUMAN_WIN_SCORE

    if len(get_available_moves(board)) == 0:
        return DRAW_SCORE

    return None


def minimax(board, depth, is_maximizing):
    """
    Minimax recursively explores all possible moves.

    AI tries to maximize the score.
    Human is assumed to minimize the AI's score.

    No depth limit is used because Tic-Tac-Toe is small.
    """

    if is_terminal(board):
        score = evaluate(board)

        # Prefer quicker wins and delay unavoidable losses.
        if score == AI_WIN_SCORE:
            return score - depth

        if score == HUMAN_WIN_SCORE:
            return score + depth

        return DRAW_SCORE

    if is_maximizing:
        best_score = float("-inf")

        for move in get_available_moves(board):
            apply_move(board, move, AI)

            score = minimax(board, depth + 1, False)

            undo_move(board, move)

            best_score = max(best_score, score)

        return best_score

    else:
        best_score = float("inf")

        for move in get_available_moves(board):
            apply_move(board, move, HUMAN)

            score = minimax(board, depth + 1, True)

            undo_move(board, move)

            best_score = min(best_score, score)

        return best_score


def find_best_move(board):
    """Return the optimal move and its Minimax score."""
    best_score = float("-inf")
    best_move = None

    for move in get_available_moves(board):
        apply_move(board, move, AI)

        score = minimax(board, 1, False)

        undo_move(board, move)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move, best_score


# ============================================================
# GRAPHICAL INTERFACE
# ============================================================

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe | Minimax AI")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.board = create_board()
        self.game_over = False

        self.human_wins = 0
        self.ai_wins = 0
        self.draws = 0

        self.buttons = []

        self.build_interface()
        self.update_status("Your turn — make a move!")

    def build_interface(self):
        """Create all interface elements."""

        main_frame = tk.Frame(
            self.root,
            bg=BG_COLOR,
            padx=28,
            pady=24
        )
        main_frame.pack()

        # Title
        tk.Label(
            main_frame,
            text="TIC-TAC-TOE",
            font=("Segoe UI", 25, "bold"),
            fg=TEXT_COLOR,
            bg=BG_COLOR
        ).pack()

        tk.Label(
            main_frame,
            text="ARTIFICIAL INTELLIGENCE  /  MINIMAX",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED_COLOR,
            bg=BG_COLOR
        ).pack(pady=(4, 18))

        # Score panel
        score_frame = tk.Frame(
            main_frame,
            bg=PANEL_COLOR,
            padx=12,
            pady=12
        )
        score_frame.pack(fill="x", pady=(0, 16))

        self.human_score_label = tk.Label(
            score_frame,
            text="YOU (X): 0",
            font=("Segoe UI", 10, "bold"),
            fg=X_COLOR,
            bg=PANEL_COLOR
        )
        self.human_score_label.pack(side="left", expand=True)

        self.draw_score_label = tk.Label(
            score_frame,
            text="DRAWS: 0",
            font=("Segoe UI", 10, "bold"),
            fg=TEXT_COLOR,
            bg=PANEL_COLOR
        )
        self.draw_score_label.pack(side="left", expand=True)

        self.ai_score_label = tk.Label(
            score_frame,
            text="AI (O): 0",
            font=("Segoe UI", 10, "bold"),
            fg=O_COLOR,
            bg=PANEL_COLOR
        )
        self.ai_score_label.pack(side="left", expand=True)

        # Game board
        board_frame = tk.Frame(main_frame, bg=BG_COLOR)
        board_frame.pack()

        for row in range(BOARD_SIZE):
            button_row = []

            for col in range(BOARD_SIZE):
                button = tk.Button(
                    board_frame,
                    text="",
                    font=("Segoe UI", 32, "bold"),
                    fg=TEXT_COLOR,
                    bg=CELL_COLOR,
                    activebackground=CELL_HOVER,
                    activeforeground=TEXT_COLOR,
                    disabledforeground=TEXT_COLOR,
                    relief="flat",
                    bd=0,
                    width=4,
                    height=2,
                    cursor="hand2",
                    command=lambda r=row, c=col: self.on_cell_click(r, c)
                )

                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

                button_row.append(button)

            self.buttons.append(button_row)

        # Status message
        self.status_label = tk.Label(
            main_frame,
            text="",
            font=("Segoe UI", 11, "bold"),
            fg=TEXT_COLOR,
            bg=BG_COLOR,
            wraplength=340,
            height=2
        )
        self.status_label.pack(pady=(14, 8))

        # Minimax information
        self.ai_info_label = tk.Label(
            main_frame,
            text="AI algorithm: Minimax | Full search",
            font=("Segoe UI", 9),
            fg=MUTED_COLOR,
            bg=BG_COLOR
        )
        self.ai_info_label.pack(pady=(0, 16))

        # New game button
        self.new_game_button = tk.Button(
            main_frame,
            text="NEW GAME",
            font=("Segoe UI", 11, "bold"),
            fg="#FFFFFF",
            bg=ACCENT_COLOR,
            activebackground="#4F46E5",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.reset_game,
            padx=20,
            pady=11
        )
        self.new_game_button.pack(fill="x")

        tk.Label(
            main_frame,
            text="You play as X  •  AI plays as O",
            font=("Segoe UI", 9),
            fg=MUTED_COLOR,
            bg=BG_COLOR
        ).pack(pady=(14, 0))

    def update_status(self, message, color=TEXT_COLOR):
        """Update the status message."""
        self.status_label.config(text=message, fg=color)

    def update_scoreboard(self):
        """Refresh the displayed scores."""
        self.human_score_label.config(
            text=f"YOU (X): {self.human_wins}"
        )
        self.ai_score_label.config(
            text=f"AI (O): {self.ai_wins}"
        )
        self.draw_score_label.config(
            text=f"DRAWS: {self.draws}"
        )

    def on_cell_click(self, row, col):
        """Handle a human player's click."""

        if self.game_over or self.board[row][col] != EMPTY:
            return

        # Human makes a move
        apply_move(self.board, (row, col), HUMAN)
        self.update_cell(row, col, HUMAN)

        if self.finish_if_terminal():
            return

        # Temporarily prevent further clicks while AI calculates.
        self.set_board_enabled(False)
        self.update_status("AI is analyzing possible moves...", O_COLOR)
        self.root.update_idletasks()

        # AI chooses its optimal move.
        move, score = find_best_move(self.board)

        if move is not None:
            apply_move(self.board, move, AI)
            self.update_cell(move[0], move[1], AI)

        self.ai_info_label.config(
            text=f"Minimax algorithm | Evaluation score: {score}"
        )

        if self.finish_if_terminal():
            return

        self.set_board_enabled(True)
        self.update_status("Your turn — make a move!", X_COLOR)

    def update_cell(self, row, col, player):
        """Update the appearance of one cell."""
        color = X_COLOR if player == HUMAN else O_COLOR

        self.buttons[row][col].config(
            text=player,
            fg=color,
            disabledforeground=color,
            bg=PANEL_COLOR,
            state="disabled"
        )

    def set_board_enabled(self, enabled):
        """Enable only empty cells when the game is active."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == EMPTY and not self.game_over:
                    state = "normal" if enabled else "disabled"

                    self.buttons[row][col].config(
                        state=state,
                        bg=CELL_COLOR
                    )

    def finish_if_terminal(self):
        """Check the result and update the interface."""
        winner = check_winner(self.board)

        if winner == HUMAN:
            self.game_over = True
            self.human_wins += 1
            self.update_status("You won! Congratulations!", WIN_COLOR)

        elif winner == AI:
            self.game_over = True
            self.ai_wins += 1
            self.update_status("AI wins! Try again.", O_COLOR)

        elif not get_available_moves(self.board):
            self.game_over = True
            self.draws += 1
            self.update_status("It's a draw!", TEXT_COLOR)

        else:
            return False

        self.set_board_enabled(False)
        self.update_scoreboard()
        return True

    def reset_game(self):
        """Start a new round without resetting the score."""
        self.board = create_board()
        self.game_over = False

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.buttons[row][col].config(
                    text="",
                    state="normal",
                    bg=CELL_COLOR,
                    fg=TEXT_COLOR,
                    disabledforeground=TEXT_COLOR
                )

        self.ai_info_label.config(
            text="AI algorithm: Minimax | Full search"
        )

        self.update_status("Your turn — make a move!", X_COLOR)


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main():
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
