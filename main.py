
# ============================================================
# AI Laboratory Work 2
# Tic-Tac-Toe: Human vs AI
# Algorithm: Minimax
# ============================================================

BOARD_SIZE = 3

HUMAN = "X"
AI = "O"
EMPTY = " "

AI_WIN_SCORE = 10
HUMAN_WIN_SCORE = -10
DRAW_SCORE = 0


def create_board():
    """Create an empty 3x3 game board."""
    return [[EMPTY for _ in range(BOARD_SIZE)]
            for _ in range(BOARD_SIZE)]


def print_board(board):
    """Display the game board in the console."""
    print("\n")
    print("       1   2   3")
    print("     +---+---+---+")

    for row in range(BOARD_SIZE):
        print(
            f"  {row + 1}  | "
            + " | ".join(board[row])
            + " |"
        )
        print("     +---+---+---+")

    print()


def get_available_moves(board):
    """Return all empty cells as (row, column) pairs."""
    moves = []

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY:
                moves.append((row, col))

    return moves


def apply_move(board, move, player):
    """Place a player's symbol on the board."""
    row, col = move
    board[row][col] = player


def undo_move(board, move):
    """Undo a simulated move during Minimax search."""
    row, col = move
    board[row][col] = EMPTY


def check_winner(board):
    """
    Return the winning symbol if a player has won.
    Return None if there is no winner.
    """

    # Check rows
    for row in range(BOARD_SIZE):
        if (board[row][0] != EMPTY
                and board[row][0] == board[row][1]
                == board[row][2]):
            return board[row][0]

    # Check columns
    for col in range(BOARD_SIZE):
        if (board[0][col] != EMPTY
                and board[0][col] == board[1][col]
                == board[2][col]):
            return board[0][col]

    # Check the main diagonal
    if (board[0][0] != EMPTY
            and board[0][0] == board[1][1]
            == board[2][2]):
        return board[0][0]

    # Check the opposite diagonal
    if (board[0][2] != EMPTY
            and board[0][2] == board[1][1]
            == board[2][0]):
        return board[0][2]

    return None


def is_terminal(board):
    """Check whether the game has ended."""
    if check_winner(board) is not None:
        return True

    return len(get_available_moves(board)) == 0


def evaluate(board):
    """
    Evaluate a terminal game state:
    AI win    = +10
    Human win = -10
    Draw      = 0
    """
    winner = check_winner(board)

    if winner == AI:
        return AI_WIN_SCORE

    if winner == HUMAN:
        return HUMAN_WIN_SCORE

    if is_terminal(board):
        return DRAW_SCORE

    # Non-terminal positions are not evaluated here.
    return None


def minimax(board, depth, is_maximizing):
    """
    Recursively search the game tree.

    AI (maximizing player) chooses the maximum score.
    Human (minimizing player) chooses the minimum score.
    The entire game tree is searched until a terminal state.
    """

    # Base case: the game has ended
    if is_terminal(board):
        score = evaluate(board)

        # Prefer faster AI wins and slower AI losses
        if score == AI_WIN_SCORE:
            return score - depth

        if score == HUMAN_WIN_SCORE:
            return score + depth

        return DRAW_SCORE

    if is_maximizing:
        # AI tries to maximize the score
        best_score = float("-inf")

        for move in get_available_moves(board):
            apply_move(board, move, AI)

            score = minimax(board, depth + 1, False)

            undo_move(board, move)

            best_score = max(best_score, score)

        return best_score

    else:
        # Human is assumed to choose the best response,
        # minimizing the AI's score.
        best_score = float("inf")

        for move in get_available_moves(board):
            apply_move(board, move, HUMAN)

            score = minimax(board, depth + 1, True)

            undo_move(board, move)

            best_score = min(best_score, score)

        return best_score


def find_best_move(board):
    """Find the optimal move for the AI."""
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


def human_move(board):
    """Ask the human player to enter a move."""
    while True:
        try:
            choice = input(
                "Your move (row and column, e.g. 2 3): "
            ).strip()

            parts = choice.split()

            if len(parts) != 2:
                print("Enter two numbers: row and column.")
                continue

            row = int(parts[0]) - 1
            col = int(parts[1]) - 1

            if not (0 <= row < BOARD_SIZE
                    and 0 <= col < BOARD_SIZE):
                print("Invalid coordinates. Choose 1, 2, or 3.")
                continue

            if board[row][col] != EMPTY:
                print("That cell is already occupied.")
                continue

            apply_move(board, (row, col), HUMAN)
            break

        except ValueError:
            print("Invalid input. Please enter two numbers.")


def announce_result(board):
    """Display the final result."""
    winner = check_winner(board)

    print_board(board)

    if winner == HUMAN:
        print("Congratulations! You won!")
    elif winner == AI:
        print("AI wins! Better luck next time.")
    else:
        print("It's a draw!")


def main():
    """Main game loop: Human vs AI."""
    print("=" * 42)
    print("       TIC-TAC-TOE: HUMAN VS AI")
    print("          AI algorithm: Minimax")
    print("=" * 42)

    print("\nYou play as X.")
    print("AI plays as O.")
    print("Enter the row and column to make a move.")
    print("Example: 2 3 means row 2, column 3.")

    board = create_board()

    # Human always makes the first move
    while not is_terminal(board):
        print_board(board)
        human_move(board)

        if is_terminal(board):
            break

        print("\nAI is analyzing possible moves...")

        move, score = find_best_move(board)

        if move is not None:
            apply_move(board, move, AI)
            print(
                f"AI chose row {move[0] + 1}, "
                f"column {move[1] + 1}."
            )
            print(f"Minimax score: {score}")

    announce_result(board)


if __name__ == "__main__":
    main()
