"""
An AI player for Mancala.
"""

# Some potentially helpful libraries
import random
import math
import time

# You can use the functions in mancala_game to write your AI. Import methods you need.
from mancala_game import Board, get_possible_moves, eprint, play_move, MCTS, end_game

cache = {}  # Use this variable for your state cache; Use it if caching is on


# Description of the compute_heuristic():
# The most easy and efficient way to earn stones( and beat your opponent) is to try
# creating empty pocket faster than your enemy. Thus, having an empty pockets are extremely important.
# My heuristic takes care of the empty pocket for each recursion. If an empty pocket has been spotted,
# the current player will move to the empty pocket and collect stones from the corresponding pocket of
# enemy's spot. So, we can easily win the game.
# I also notice that we should not put too many stones in one pocket.
# This will increase the risk of letting the opponent take all stones from this pocket.
# So, I'm playing smart by sending stones equally to several pockets.
# If the opponent forms an empty pocket, I will not lose that many stones since I reduce the risk.


# Implement the below functions. You are allowed to define additional functions that you believe will come in handy.
def compute_utility(board, side):
    # IMPLEMENT!
    """
    Method to compute the utility value of board. This is equal to the number of stones of the mancala
    of a given player, minus the number of stones in the opposing player's mancala.
    INPUT: a game state, the player that is in control
    OUTPUT: an integer that represents utility
    """
    score = 0
    player_A = board.mancalas[1]
    player_B = board.mancalas[0]
    # print(player_A, player_B)
    if side == 0:  # Player B
        return player_B - player_A
    elif side == 1:  # Player A
        return player_A - player_B
    else:
        return 0


def compute_heuristic(board, color):
    # IMPLEMENT!
    """
    Method to compute the heuristic value of a specific state of the board.
    INPUT: a game state, the player that is in control, the depth limit for the search
    OUTPUT: an integer that represents heuristic value
    """
    pocket_B = board.pockets[0]
    pocket_A = board.pockets[1]
    player_B = board.mancalas[0]
    player_A = board.mancalas[1]
    if color == 0:
        for pocket in pocket_B:
            if pocket == 0:
                count = pocket_A[pocket]
                player_B += count

        return player_B
    else:
        for pockets in pocket_A:
            if pockets == 0:
                count = pocket_B[pockets]
                player_A += count

        return player_A


# def is_reachable(board, color):
#     if color == 1:
#         pocket_A = board.pockets[1]
#         lst = []
#         moves = get_possible_moves(board, color)
#         # print(moves, board.pockets[1])
#         for item in range(0, len(moves)):
#             match = (moves[item], pocket_A[item])
#             lst.append(match)


################### MINIMAX METHODS ####################
def select_move_minimax(board, color, limit=-1, caching=False):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using the MINIMAX ALGORITHM. The return value is 
    an integer i, where i is the pocket that the player on side 'color' should select.
    INPUT: a game state, the player that is in control, the depth limit for the search, and a boolean that determines whether state caching is on or not
    OUTPUT: an integer that represents a move
    """
    # if color == 1:
    #     result = minimax_max(board, color, limit, caching)
    #     return result
    # elif color == 0:
    #     result = minimax_min(board, color, limit, caching)
    #     return result
    return minimax_max(board, color, limit, caching)[1]


def minimax_max(board, color, limit, caching):
    rival = 0
    if color == 0:
        rival = 1
    elif color == 1:
        rival = 0
    # if caching:
    #     if (board, color) in cache:
    #         return cache[(board, color)]
    # if caching and board in cache:
    #     pass

    if limit == 0 or len(get_possible_moves(board, color)) == 0:
        if (board in cache) and caching:
            cache[board] = compute_utility(board, color)
        return compute_utility(board, color), None

    else:
        maximum = float("-inf")
        solution = None
        lst = []
        for move in get_possible_moves(board, color):
            new_board = play_move(board, color, move)
            updated_utility_score = minimax_min(new_board, rival, limit - 1, caching)[0]
            lst.append(updated_utility_score)
            if max(lst) > maximum:
                maximum = max(lst)
                solution = move

        # if caching:
        #     cache[board] = maximum

        return maximum, solution


def minimax_min(board, color, limit, caching):
    rival = 0
    if color == 0:
        rival = 1
    elif color == 1:
        rival = 0
    # if caching:
    #     if (board, color) in cache:
    #         return cache[(board, color)]
    # if caching and board in cache:
    #     pass

    if limit == 0 or len(get_possible_moves(board, color)) == 0:
        if board not in cache and caching:
            cache[board] = compute_utility(board, rival)
        return compute_utility(board, rival), None

    else:
        minimum = float("inf")
        solution = None
        lst = []
        lst1 = []
        for move in get_possible_moves(board, color):
            new_board = play_move(board, color, move)
            new_utility_score = minimax_max(new_board, rival, limit - 1, caching)[0]
            lst.append(new_utility_score)
            if min(lst) < minimum:
                minimum = min(lst)
                solution = move
                lst1.append(solution)
        # if caching:
        #     cache[board] = minimum

        return minimum, random.choice(lst1)


################### ALPHA-BETA METHODS ####################
def select_move_alphabeta(board, color, limit=-1, caching=False):
    # IMPLEMENT!
    """
    Given a board and a player color, decide on a move using the ALPHABETA ALGORITHM. The return value is 
    an integer i, where i is the pocket that the player on side 'color' should select.
    INPUT: a game state, the player that is in control, the depth limit for the search, and a boolean that determines if state caching is on or not
    OUTPUT: an integer that represents a move
    """
    alpha = float("-inf")
    beta = float("inf")
    return alphabeta_max(board, color, alpha, beta, limit, caching)[1]


dict = {}
dict1 = {}


def alphabeta_max(board, color, alpha, beta, limit, caching):
    rival = 0
    if color == 0:
        rival = 1
    elif color == 1:
        rival = 0
    # if caching:
    #     if (board, color) in cache:
    #         return cache[(board, color)]
    # if caching and board in cache:
    #     pass

    if limit == 0 or len(get_possible_moves(board, color)) == 0:
        if (board in dict) and caching:
            dict[board] = alpha, beta
        return compute_utility(board, color), None

    else:
        maximum = float("-inf")
        solution = None
        lst = []
        for move in get_possible_moves(board, color):
            new_board = play_move(board, color, move)
            updated_utility_score = alphabeta_min(new_board, rival, alpha, beta, limit - 1, caching)[0]
            lst.append(updated_utility_score)
            if max(lst) > maximum:
                maximum = max(lst)
                solution = move

            alpha = max(alpha, maximum)
            if beta <= alpha:
                break

        return alpha, solution


def alphabeta_min(board, color, alpha, beta, limit, caching):
    rival = 0
    if color == 0:
        rival = 1
    elif color == 1:
        rival = 0
    # if caching:
    #     if (board, color) in cache:
    #         return cache[(board, color)]
    # if caching and board in cache:
    #     pass

    if limit == 0 or len(get_possible_moves(board, color)) == 0:
        if board not in dict1 and caching:
            dict1[board] = alpha, beta
        return compute_utility(board, rival), None

    else:
        minimum = float("inf")
        solution = None
        lst = []
        for move in get_possible_moves(board, color):
            new_board = play_move(board, color, move)
            new_utility_score = alphabeta_max(new_board, rival, alpha, beta, limit - 1, caching)[0]
            lst.append(new_utility_score)
            if min(lst) < minimum:
                minimum = min(lst)
                solution = move

            beta = min(beta, minimum)
            if beta <= alpha:
                break

        return beta, solution


################### MCTS METHODS ####################
def ucb_select(board, mcts_tree):
    # IMPLEMENT! This is the only function of MCTS that will be marked as a part of the assignment. Feel free to implement the others, but only if you like.
    """
    Given a board and its MCTS tree, select and return the successive state with the highest UCB
    INPUT: a board state and an MCTS tree
    OUTPUT: the successive state of the input board that corresponds with the max UCB value in the tree.
    """
    # Hint: You can encode this as follows:
    # 1. Cycle thru the successors of the given board.
    # 2. Calculate the UCB values for the successors, given the input tree
    # 3. Return the successor with the highest UCB value
    new_dict = {}
    for s in mcts_tree.successors.get(board):
        # print(mcts_tree.counts.get(board))
        # print(mcts_tree.counts[s])

        ucb = mcts_tree.rewards[s] + mcts_tree.weight * (math.sqrt(math.log(mcts_tree.counts.get(board)) / s[1]))
        # print(ucb)
        new_dict[s] = ucb
    maximum = max(new_dict.values())
    for key in new_dict.keys():
        if new_dict.get(key) == maximum:
            return key
    return None


#######################################################################
#######################################################################
####### IMPLEMENTATION OF ALL MCTS METHODS BELOW IS OPTIONAL ###############
#######################################################################
#######################################################################

def choose_move(board, color, mcts_tree):
    # IMPLEMENT! (OPTIONAL)
    '''choose a move'''
    '''INPUT: a game state, the player that is in control and an MCTS tree'''
    '''OUTPUT: a number representing a move for the player tat is in control'''
    # Encoding this method is OPTIONAL.  You will want it to
    # 1. See if a given game state is in the MCTS tree.
    # 2. If yes, return the move that is associated with the highest average reward in the tree (from the perspective of the player 'color')
    # 3. If no, return a random move
    raise RuntimeError("Method not implemented")  # Replace this line!


def rollout(board, color, mcts_tree):
    # IMPLEMENT! (OPTIONAL)
    '''rollout the tree!'''
    '''INPUT: a game state that will be at the start of the path, the player that is in control and an MCTS tree (see class def in mancala_game)'''
    '''OUTPUT: nothing!  Just adjust the MCTS tree statistics as you roll out.'''
    # You will want it to:
    # 1. Find a path from the root of the tree to a leaf based on ucs stats (use select_path(board, color, mctsree))
    # 2. Expand the last state in that path and add all the successors to the tree (use expand_leaf(board, color, mctsree))
    # 3. Simulate game play from the final state to a terminal and derive the reward
    # 4. Back-propagate the reward all the way from the terminal to the root of the MCTS tree
    raise RuntimeError("Method not implemented")  # Replace this line!


def select_path(board, color, mcts_tree):
    # IMPLEMENT! (OPTIONAL)
    '''Find a path from the root of the tree to a leaf based on ucs stats'''
    '''INPUT: a game state that will be at the start of the path, the player that is in control and an MCTS tree (see class def in mancala_game)'''
    '''OUTPUT: A list of states that leads from the root of the MCTS tree to a leaf.'''
    # You will want it to return a path from the board provided to a
    # leaf of the MCTS tree based on ucs stats (select_path(board, mctsree)). You can encode this as follows:
    # Repeat:
    # 1. Add the state to the path
    # 2. Check to see if the state is a terminal.  If yes, return the path.
    # 3. If no, check to see if any successor of the state is a terminal.  If yes, add any unexplored terminal to the path and return.
    # 5. If no, descend the MCTS tree a level to select a new state based on the UCT criteria.
    raise RuntimeError("Method not implemented")  # Replace this line!


def expand_leaf(board, color, mcts_tree):
    # IMPLEMENT! (OPTIONAL)
    '''Expand a leaf in the mcts tree'''
    '''INPUT: a game state that will be at the start of the path, the player that is in control and an MCTS tree (see class def in mancala_game)'''
    '''OUTPUT: nothing!  Just adjust the MCTS tree statistics as you roll out.'''
    # If the given state already exists in the tree, do nothing
    # Else, add the successors of the state to the tree.
    raise RuntimeError("Method not implemented")  # Replace this line!


def simulate(board, color):
    # IMPLEMENT! (OPTIONAL)
    '''simulate game play from a state to a leaf'''
    '''INPUT: a game state, the player that is in control'''
    '''OUTPUT: a reward that the controller of the tree can hope to get from this state!'''
    # You can encode this as follows:
    # 1. Get all the possible moves from the state. If there are none, return the reward that the player in control can expect to get from the state.
    # 2. Select a moves at random, and play it to generate a new state
    # 3. Repeat.
    # Remember:
    #  -- the reward the controlling player receives at one level will be the OPPOSITE of the reward at the next level!
    #  -- at one level the player in control will play a move, and at the next his or her opponent will play a move!
    raise RuntimeError("Method not implemented")  # Replace this line!


def backprop(path, reward, mcts_tree):
    # IMPLEMENT! (OPTIONAL)
    '''backpropagate rewards a leaf to the root of the tree'''
    '''INPUT: the path leading from a state to a terminal, the reward to propagate, and an MCTS tree'''
    '''OUTPUT: nothing!  Just adjust the MCTS tree statistics as you roll out.'''
    # You can encode this as follows:
    # FROM THE BACK TO THE FRONT OF THE PATH:
    # 1. Update the number of times you've seen a given state in the MCTS tree
    # 2. Update the reward associated with that state in the MCTS tree
    # 3. Continue
    # Remember:
    #  -- the reward one level will be the OPPOSITE of the reward at the next level!  Make sure to update the rewards accordingly
    raise RuntimeError("Method not implemented")  # Replace this line!


def select_move_mcts(board, color, weight=1, numsamples=50):
    # IMPLEMENT! (OPTIONAL)
    mcts_tree = MCTS(weight)  # Initialize your MCTS tree
    for _ in range(numsamples):  # Sample the tree numsamples times
        # In here you'll want to encode a 'rollout' for each iteration
        # store the results of each rollout in the MCTS tree (mcts_tree)
        pass  # Replace this line!

    # Then, at the end of your iterations, choose the best move, according to your tree (ie choose_move(board, color, mcts_tree))
    raise RuntimeError("Method not implemented")  # Replace this line!


#######################################################################
#######################################################################
################### END OF OPTIONAL FUNCTIONS #########################
#######################################################################
#######################################################################

def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Mancala AI")  # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0])  # Player color
    limit = int(arguments[1])  # Depth limit
    CACHING = int(arguments[2])  # caching or no?
    algorithm = int(arguments[3])  # Minimax, Alpha Beta, or MCTS

    if (algorithm == 2):  # Implement this only if you really want to!!
        eprint("Running MCTS")
        limit = -1  # Limit is irrelevant to MCTS!!
    elif (algorithm == 1):
        eprint("Running ALPHA-BETA")
    else:
        eprint("Running MINIMAX")

    if (CACHING == 1):
        eprint("Caching is ON")
    else:
        eprint("Caching is OFF")

    if (limit == -1):
        eprint("Depth Limit is OFF")
    else:
        eprint("Depth Limit is ", limit)

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()

        if status == "FINAL":  # Game is over.
            print
        else:
            pockets = eval(input())  # Read in the pockets on the board
            mancalas = eval(input())  # Read in the mancalas on the board
            board = Board(pockets, mancalas)  # turn info into an object

            # Select the move and send it to the manager
            if (algorithm == 2):
                move = select_move_mcts(board, color, numsamples=50)  # 50 samples per iteration by default
            elif (algorithm == 1):
                move = select_move_alphabeta(board, color, limit, bool(CACHING))
            else:
                move = select_move_minimax(board, color, limit, bool(CACHING))

            print("{}".format(move))


if __name__ == "__main__":
    run_ai()
