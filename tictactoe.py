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
    # Helper function for the maximizing player (X)
    def max_value(board):
        # If the game is over, return the utility of the board
        if terminal(board):
            return utility(board)
        
        v = -math.inf  # Start with the worst possible value for maximizer
        
        # Explore all possible moves
        for action in actions(board):
            # Update the best value by comparing it with the result of min_value
            v = max(v, min_value(result(board, action)))
        
        return v

    # Helper function for the minimizing player (O)
    def min_value(board):
        # If the game is over, return the utility of the board
        if terminal(board):
            return utility(board)
        
        v = math.inf  # Start with the worst possible value for minimizer
        
        # Explore all possible moves
        for action in actions(board):
            # Update the best value by comparing it with the result of max_value
            v = min(v, max_value(result(board, action)))
        
        return v

    # If the game is already over, there's no move to make
    if terminal(board):
        return None

    # Determine which player's turn it is
    current_player = player(board)
    best_action = None  # This will store the best move found

    # If it's X's turn (maximizing player)
    if current_player == X:
        best_score = -math.inf  # Start with the worst possible score for maximizer
        
        # Explore all possible moves
        for action in actions(board):
            # Evaluate the result of the move using min_value
            score = min_value(result(board, action))
            
            # If this move is better than the current best, update
            if score > best_score:
                best_score = score
                best_action = action

    # If it's O's turn (minimizing player)
    else:
        best_score = math.inf  # Start with the worst possible score for minimizer
        
        # Explore all possible moves
        for action in actions(board):
            # Evaluate the result of the move using max_value
            score = max_value(result(board, action))
            
            # If this move is better than the current best, update
            if score < best_score:
                best_score = score
                best_action = action

    # Return the action that leads to the optimal outcome
    return best_action
