"""
Tic Tac Toe Player
"""

import math
from random import randint
from copy import deepcopy


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return None

    if board == initial_state():
        return X

    X_count = 0
    O_count = 0

    for row in range(3):
        for column in range(3):
            if board[row][column] == X:
                    X_count += 1
            elif board[row][column] == O:
                    O_count += 1
    return X if X_count <= O_count else O
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                actions.add((row, column))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    new_board = deepcopy(board)
    current_player = player(new_board)

    if new_board[i][j] is not EMPTY:
        raise Exception("Invalid action.")
    else:
        new_board[i][j] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    row_check = lambda row, player: board[row][0] == player and board[row][1] == player and board[row][2] == player
    column_check = lambda column, player: board[0][column] == player and board[1][column] == player and board[2][column] == player
    diag_check = lambda player: board[0][2] == player and board[1][1] == player and board[2][0] == player
    diag_2_check = lambda player: board[0][0] == player and board[1][1] == player and board[2][2] == player
    rows_check = lambda player: [row_check(row, player) for row in range(3)]
    columns_check = lambda player: [column_check(column, player) for column in range(3)]
    winn_check = lambda player: rows_check(player) + columns_check(player) + [diag_check(player), diag_2_check(player)]
    if any(winn_check(X)):
        return X
    if any(winn_check(O)):
        return O


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or all(board[0]+board[1]+board[2]):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0


def max_val(state):
    if terminal(state):
        return utility(state)
    v = -math.inf
    for action in actions(state):
        v = max(v, min_val(result(state, action)))
    return v


def min_val(state):
    if terminal(state):
        return utility(state)
    v = math.inf
    for action in actions(state):
        v = min(v, max_val(result(state, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if board == initial_state():
        i, j = randint(0, 2), randint(0, 2)
        return (i, j)
    
    p = player(board)
    if p == X:
        v = -math.inf
        for action in actions(board):
            value = min_val(result(board, action))
            if v < value:
                best_action = action
                v = value
    elif p == O:
        v = math.inf
        for action in actions(board):
            value = max_val(result(board, action))
            if v > value:
                best_action = action
                v = value
    return best_action