"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    # Start with an empty 3x3 board
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # X goes first, then alternate turns
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    return X if x_count <= o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Find all empty spots on the board
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Make sure the action is valid
    if action not in actions(board):
        raise ValueError("Invalid action")
    
    # Copy the board and apply the move
    i, j = action
    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows, columns, and diagonals for three in a row
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
        
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Game is over if someone wins or if the board is full
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won, -1 if O has won, 0 otherwise.
    """
    # Evaluate the game result
    if winner(board) == X:
        return 1
    
    elif winner(board) == O:
        return -1
    
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Helper for maximizing player (X)
    def max_value(board):
        if terminal(board):
            return utility(board)
        
        v = -math.inf
        
        # Explore all possible moves
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
            
        return v

    # Helper for minimizing player (O)
    def min_value(board):
        if terminal(board):
            return utility(board)
        
        v = math.inf
        
        # Explore all possible moves
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
            
        return v

    # If the game is over, no moves are left
    if terminal(board):
        return None

    # Choose the best move based on whose turn it is
    current_player = player(board)

    # Check for an immediate win or block
    if current_player == X:
        for action in actions(board):
            if utility(result(board, action)) == 1:
                return action  # Return the winning move directly
    else:
        for action in actions(board):
            if utility(result(board, action)) == -1:
                return action  # Block the winning move directly

    # If no immediate win or block, proceed with minimax evaluation
    if current_player == X:
        _, move = max((min_value(result(board, action)), action) for action in actions(board))
    else:
        _, move = min((max_value(result(board, action)), action) for action in actions(board))

    return move
