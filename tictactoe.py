"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

DEPTH = 5
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
    if not terminal(board):
        cnt_x = 0
        cnt_o = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    continue
                elif board[i][j] == X:
                    cnt_x += 1
                else:
                    cnt_o += 1

        if cnt_x <= cnt_o:
            return X
        else:
            return O
    else:
        return None


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    x = action[0]
    y = action[1]
    if x < 0 or x > 2 or y < 0 or y > 2 or not board[x][y] == EMPTY:
        raise ValueError
    temp_board = deepcopy(board)
    temp_board[x][y] = player(board)
    return temp_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    chances = [X, O]
    for chance in chances:
        for row in range(3):
            if list(chance)*3 == board[row]:
                return chance
        for column in range(3):
            if [[chance] for i in range(3)] == [[board[row][column]] for row in range(3)]:
                return chance
        if board[0][0] == chance and board[1][1] == chance and board[2][2] == chance:
            return chance
        if board[0][2] == chance and board[1][1] == chance and board[2][0] == chance:
            return chance
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None:
        return True
    if not any(EMPTY in sublist for sublist in board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    final = winner(board)
    if final == X:
        return 1
    elif final == O:
        return -1
    else:
        return 0


def min_target(board, depth, alpha, beta):
    """
    Returns min_score for each board state recursively reached.
    """
    if terminal(board) or depth == DEPTH:
        return utility(board)

    best_val = math.inf
    for action in actions(board):
        val = max_target(result(board, action), depth+1, alpha, beta)
        best_val = min(val, best_val)
        beta = min(beta, best_val)
        if beta <= alpha:
            break

    return best_val


def max_target(board, depth, alpha, beta):
    """
    Returns max_score for each board state recursively reached.
    """
    if terminal(board) or depth == DEPTH:
        return utility(board)

    best_val = -math.inf
    for action in actions(board):
        val = min_target(result(board, action), depth+1, alpha, beta)
        best_val = max(best_val, val)
        alpha = max(alpha, best_val)
        if beta <= alpha:
            break

    return best_val


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return utility(board)

    chance = player(board)
    if chance == X:
        v = -math.inf
        best_action = None

        for action in actions(board):
            v_temp = min_target(result(board, action), 0, -math.inf, math.inf)

            if v_temp > v:
                best_action = action
                v = v_temp

    else:
        v = math.inf
        best_action = None

        for action in actions(board):
            v_temp = max_target(result(board, action), 0, -math.inf, math.inf)

            if v_temp < v:
                best_action = action
                v = v_temp

    return best_action
