"""
Gomoku.
"""
# Imports.
import copy

# Board constants.
X = "X"
O = "O"
E = None

# Global atributtes.
board_width = 6
board_heigth = 6
match_number = 5
last_action = (0, 0)
last_player = E
"""
prefabricated_board = [ [E, E, E, E, E, E, E, E],
                        [E, E, E, E, E, E, E, E],
                        [E, E, E, E, E, E, E, E],
                        [E, E, E, E, E, E, E, E],
                        [E, E, E, E, E, E, E, E],
                        [E, E, E, E, E, E, E, E],
                        [E, E, E, E, E, E, E, E],
                        [E, E, E, E, E, E, E, E]]
prefabricated_board = [ ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7"],
                        ["B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"],
                        ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"],
                        ["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7"],
                        ["E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7"],
                        ["F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7"],
                        ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7"],
                        ["H0", "H1", "H2", "H3", "H4", "H5", "H6", "H7"]]
"""


def clamp(number, minimum_value, maximum_value):
    return max(min(number, maximum_value), minimum_value)


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[E] * board_width for cell in range(board_heigth)]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Martín Salvador Sosa - Tinincho.
    player_tokens = 0

    for row in board:
        for element in row:
            if element == E:
                player_tokens += 1

    player_tokens = (board_width * board_heigth) - player_tokens

    if player_tokens % 2 == 0:
        return X

    return O


def actions(board):
    """
    Returns set of all possible actions (row, column) available on the board.
    """
    actions = set()

    for row in enumerate(board):
        for column in enumerate(row[1]):
            if column[1] == E:
                actions.add((row[0], column[0]))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (row, column) on the board.
    """
    global last_action
    last_action = copy.deepcopy(action)
    new_board = copy.deepcopy(board)
    get_move = list(action)

    if new_board[get_move[0]][get_move[1]] == E:
        new_board[get_move[0]][get_move[1]] = player(new_board)
        return new_board

    raise Exception("Invalid action")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    last_player = X if player(board) == O else O
    current_row, current_column = last_action
    positions = [   (current_row, current_column - match_number),
                    (current_row - match_number, current_column - match_number),
                    (current_row - match_number, current_column),
                    (current_row - match_number, current_column + match_number)]
    directions = [  (0, 0, 1),
                    (1, 1, 1),
                    (2, 1, 0),
                    (3, 1, -1)]

    for get_position, direction_x, direction_y in directions:
        win_count = 0
        
        for iterator in range(0, match_number * 2 + 1):
            new_row = positions[get_position][0] + iterator * direction_x
            new_column = positions[get_position][1] + iterator * direction_y

            if new_row < 0 or new_row > board_width - 1:
                continue

            if new_column < 0 or new_column > board_heigth - 1:
                continue

            if last_player == board[new_row][new_column]:
                win_count += 1

                if win_count == match_number:
                    return last_player
            
            else:
                win_count = 0

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    for row in enumerate(board):
        for column in enumerate(row[1]):
            if board[row[0]][column[0]] == E:
                return False

            if (row[0], column[0]) == (board_width - 1, board_heigth - 1):
                return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_result = winner(board)

    if game_result == X:
        return 1

    elif game_result == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None

    total_depth = 2
    value = 0
    move = set()

    if player(board) == X:
        value = float('-inf')

        for action in actions(board):
            current_value = minimise_value(result(board, action), total_depth, float('-inf'), float('inf'))

            if current_value > value:
                move = action
                value = current_value
    else:
        value = float('inf')

        for action in actions(board):
            current_value = maximise_value(result(board, action), total_depth, float('-inf'), float('inf'))

            if current_value < value:
                move = action
                value = current_value

    return move


def maximise_value(board, depth, alpha, beta):
    """
    Check possible actions and pick the highest value.
    """
    if depth == 0 or terminal(board) == True:
        return utility(board)

    value = float('-inf')
    depth -= 1

    for action in actions(board):
        value = max(value, minimise_value(result(board, action), depth, alpha, beta))
        alpha = max(alpha, value)

        if beta <= alpha:
            break

    return value


def minimise_value(board, depth, alpha, beta):
    """
    Check possible actions and pick the lowest value.
    """
    if depth == 0 or terminal(board) == True:
        return utility(board)

    value = float('inf')
    depth -= 1

    for action in actions(board):
        value = min(value, maximise_value(result(board, action), depth, alpha, beta))
        beta = min(beta, value)

        if beta <= alpha:
            break

    return value