# chess_min.py
# Minimal console chess (movement validation, turn-taking).
# Notes: no castling, en-passant, or check/checkmate detection.

FILES = "abcdefgh"
RANKS = "12345678"

def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def parse_square(s):
    s = s.strip().lower()
    if len(s) != 2 or s[0] not in FILES or s[1] not in RANKS:
        return None
    c = FILES.index(s[0])
    r = 8 - int(s[1])
    return r, c

def square_name(r, c):
    return f"{FILES[c]}{8-r}"

def is_white(piece):
    return piece.isupper()

def is_black(piece):
    return piece.islower()

def empty(piece):
    return piece == "."

def make_board():
    # Standard chess start
    board = [["." for _ in range(8)] for _ in range(8)]
    board[0] = list("rnbqkbnr")
    board[1] = list("pppppppp")
    board[6] = list("PPPPPPPP")
    board[7] = list("RNBQKBNR")
    return board

def print_board(board):
    print("\n    a b c d e f g h")
    print("  +-----------------+")
    for r in range(8):
        row = " ".join(board[r])
        print(f"{8-r} | {row} | {8-r}")
    print("  +-----------------+")
    print("    a b c d e f g h\n")

def path_clear(board, r1, c1, r2, c2):
    dr = (r2 - r1)
    dc = (c2 - c1)
    step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
    step_c = 0 if dc == 0 else (1 if dc > 0 else -1)

    r, c = r1 + step_r, c1 + step_c
    while (r, c) != (r2, c2):
        if not empty(board[r][c]):
            return False
        r += step_r
        c += step_c
    return True

def valid_pawn(board, r1, c1, r2, c2, turn_white):
    piece = board[r1][c1]
    direction = -1 if turn_white else 1  # white goes up (towards smaller r)
    start_row = 6 if turn_white else 1

    target = board[r2][c2]

    # Forward move
    if c1 == c2:
        if not empty(target):
            return False
        if r2 == r1 + direction:
            return True
        # Two squares from start
        if r1 == start_row and r2 == r1 + 2 * direction:
            between_r = r1 + direction
            return empty(board[between_r][c1])
        return False

    # Diagonal capture
    if abs(c2 - c1) == 1 and r2 == r1 + direction:
        if empty(target):
            return False
        # capture opponent
        return (is_black(target) if turn_white else is_white(target))

    return False

def valid_knight(r1, c1, r2, c2):
    dr = abs(r2 - r1)
    dc = abs(c2 - c1)
    return (dr, dc) in [(1, 2), (2, 1)]

def valid_king(r1, c1, r2, c2):
    return max(abs(r2 - r1), abs(c2 - c1)) == 1

def valid_bishop(board, r1, c1, r2, c2):
    return abs(r2 - r1) == abs(c2 - c1) and path_clear(board, r1, c1, r2, c2)

def valid_rook(board, r1, c1, r2, c2):
    return (r1 == r2 or c1 == c2) and path_clear(board, r1, c1, r2, c2)

def valid_queen(board, r1, c1, r2, c2):
    return valid_rook(board, r1, c1, r2, c2) or valid_bishop(board, r1, c1, r2, c2)

def is_legal_move(board, r1, c1, r2, c2, turn_white):
    if not in_bounds(r1, c1) or not in_bounds(r2, c2):
        return False, "Move out of bounds."

    piece = board[r1][c1]
    if empty(piece):
        return False, "No piece on that square."

    if turn_white and not is_white(piece):
        return False, "It is White's turn."
    if (not turn_white) and not is_black(piece):
        return False, "It is Black's turn."

    target = board[r2][c2]
    if not empty(target):
        # cannot capture own piece
        if (is_white(piece) and is_white(target)) or (is_black(piece) and is_black(target)):
            return False, "You cannot capture your own piece."

    p = piece.lower()

    if p == "p":
        ok = valid_pawn(board, r1, c1, r2, c2, turn_white)
    elif p == "n":
        ok = valid_knight(r1, c1, r2, c2)
    elif p == "b":
        ok = valid_bishop(board, r1, c1, r2, c2)
    elif p == "r":
        ok = valid_rook(board, r1, c1, r2, c2)
    elif p == "q":
        ok = valid_queen(board, r1, c1, r2, c2)
    elif p == "k":
        ok = valid_king(r1, c1, r2, c2)
    else:
        ok = False

    if not ok:
        return False, "Illegal move for that piece."

    return True, ""

def make_move(board, r1, c1, r2, c2):
    board[r2][c2] = board[r1][c1]
    board[r1][c1] = "."

def main():
    board = make_board()
    turn_white = True

    print("Minimal Console Chess")
    print("Enter moves like: e2 e4   (or type 'quit')\n")

    while True:
        print_board(board)
        side = "White" if turn_white else "Black"
        move = input(f"{side} to move > ").strip().lower()

        if move in ["quit", "exit"]:
            print("Goodbye.")
            break

        parts = move.split()
        if len(parts) != 2:
            print("Please enter moves in the format: e2 e4")
            continue

        src = parse_square(parts[0])
        dst = parse_square(parts[1])
        if not src or not dst:
            print("Invalid squares. Use a1 to h8.")
            continue

        r1, c1 = src
        r2, c2 = dst

        ok, reason = is_legal_move(board, r1, c1, r2, c2, turn_white)
        if not ok:
            print("Invalid move:", reason)
            continue

        make_move(board, r1, c1, r2, c2)
        turn_white = not turn_white

if __name__ == "__main__":
    main()