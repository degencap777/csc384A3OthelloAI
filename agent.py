"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

visited_states = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    """
    computes the utility value
    :param board: tuple of tuples (represents board state)
    :param color: color of player (str)
    :return: utility value (int)
    """
    state = get_score(board)
    if color == 1:
        return state[0]-state[1]
    else:
        return state[1]-state[0]

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return 0 #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit = 0, caching = 0, depth=0):
    if color == 2:
        opponent_color = 1
    else:
        opponent_color = 2
    possible_moves = get_possible_moves(board, color)
    if possible_moves == []:
        #print("min, end, depth {}, utility {}".format(depth, compute_utility(board, opponent_color)))
        return ()
    elif limit==0:
        #print("min, at limit, depth {}, utility {}".format(depth, compute_utility(board, opponent_color)))
        if board in visited_states and caching == 1:
            utility_value = visited_states[board]
        else:
            print("not in")
            utility_value = compute_utility(board, opponent_color)
            visited_states[board] = utility_value # create new mapping
        return (utility_value, )
    else:
        #utility_values = []
        curr_min = float('inf')
        selected_move = None
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            if new_board in visited_states and caching == 1:
                utility_value = visited_states[new_board]
            else:
                node = minimax_max_node(new_board, opponent_color, limit - 1, caching, depth + 1)
                if len(node) == 0:
                    utility_value = compute_utility(new_board, opponent_color)
                elif len(node) == 1:
                    utility_value = node[0]
                else:
                    utility_value = node[1]
                if caching == 1:
                    print("not in")
                    visited_states[new_board] = utility_value
            if utility_value < curr_min:
                curr_min = utility_value
                selected_move = move
            #utility_values.append((move, utility_value))
            #print("min; depth {}; values so far: {}".format(depth, utility_values))
        # return min(utility_values, key=lambda x: x[1])
        return (selected_move, curr_min)

def minimax_max_node(board, color, limit = 0, caching = 0, depth=0): #returns highest possible utility
    #IMPLEMENT
    if color == 2:
        opponent_color = 1
    else:
        opponent_color = 2
    possible_moves = get_possible_moves(board, color)
    if possible_moves == []:
        # print("max, end, depth {}, utility {}".format(depth,compute_utility(board, color)))
        return ()
    elif limit == 0:
        # print("max, at limit, depth {}, utility {}".format(depth,compute_utility(board, color)))
        if board in visited_states and caching == 1:
            utility_value = visited_states[board]
        else:
            utility_value = compute_utility(board, opponent_color)
            if caching == 1:
                visited_states[board] = utility_value # create new mapping
        return (utility_value, )
    else:
        curr_max = float("-Inf")
        selected_move = None
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])

                node = minimax_min_node(new_board, opponent_color, limit - 1, caching, depth + 1)
                if len(node) == 0:
                    utility_value = compute_utility(new_board, color)
                elif len(node) == 1:
                    utility_value = node[0]
                else:
                    utility_value = node[1]
                if caching == 1:
                    print("not in")
                    visited_states[new_board] = utility_value
            if utility_value > curr_max:
                curr_max = utility_value
                selected_move = move
            #print("max; depth {}; values so far: {}".format(depth, utility_values))
        return (selected_move, curr_max)
    # return None

def select_move_minimax(board, color, limit=0, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enforce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    value = minimax_max_node(board, color, limit, caching)
    if len(value) == 0:
        return value
    else:
        return value[0]

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0, depth = 0):
    if color == 2:
        opponent_color = 1
    else:
        opponent_color = 2
    possible_moves = get_possible_moves(board, color)
    if possible_moves == []:
        #print("min, end, depth {}, utility {}".format(depth, compute_utility(board, opponent_color)))
        return ()
    elif limit==0:
        #print("min, at limit, depth {}, utility {}".format(depth, compute_utility(board, opponent_color)))
        return (compute_utility(board, opponent_color), )
    else:
        selected_move = None
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            node = alphabeta_max_node(new_board, opponent_color, alpha, beta, limit - 1, caching, ordering, depth+1)
            if len(node) == 0:
                beta_candidate = compute_utility(new_board, opponent_color)
            elif len(node) == 1:
                beta_candidate = node[0]
            else:
                beta_candidate = node[1]
            if beta_candidate < beta:
                beta = beta_candidate
                selected_move = move
                if alpha > beta:
                    break
            #print("min; depth {}; values so far: {}".format(depth, utility_values))
        return (selected_move, beta)

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0, depth=0):
    if color == 2:
        opponent_color = 1
    else:
        opponent_color = 2
    possible_moves = get_possible_moves(board, color)
    if possible_moves == []:
        # print("max, end, depth {}, utility {}".format(depth,compute_utility(board, color)))
        return ()
    elif limit == 0:
        # print("max, at limit, depth {}, utility {}".format(depth,compute_utility(board, color)))
        return (compute_utility(board, color),)
    else:
        selected_move = None
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            node = alphabeta_min_node(new_board, opponent_color, alpha, beta, limit - 1, caching, ordering, depth + 1)
            if len(node) == 0: # terminal
                alpha_candidate = compute_utility(new_board, color)
            elif len(node) == 1: # terminal
                alpha_candidate = node[0]
            else: # non-terminal
                alpha_candidate = node[1]
            # change alpha
            if alpha_candidate > alpha:
                alpha = alpha_candidate
                selected_move = move
                if beta < alpha:
                    break
            # print("max; depth {}; values (a,b) so far: {}, {}".format(depth, alpha, beta))
        return (selected_move, alpha)

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT
    # alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0, depth=0):

    value = alphabeta_max_node(board, color, float('-inf'), float('inf'), limit, caching, ordering)
    if len(value) == 0:
        return value
    else:
        return value[0]

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
