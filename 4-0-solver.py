#####################################
######### "The game of 4-0" #########
###### Completed by: Lisa Jian ######
#####################################

from enum import Enum

### Specific to the game 4-0 ###
def init_position():
    """
    Returns the initial position of 4-0.
    """
    return 4

def primitive(position):
    """
    Returns if the current position is a losing position.
    Assumes <code>position</code> is valid (i.e. non-negative).
    """
    if position == 0:
        return DWULT.LOSE
    return DWULT.UNKNOWN

def generate_moves(position):
    """
    Generates possible moves for the given position.
    For 4-0, we can only take away 1 or 2.
    """
    if position <= 0:
        return []
    elif position == 1:
        return [-1]
    return [-1, -2]

def do_move(position, action):
    """
    Performs the specified action on the given position
    and returns the resulting position.
    """
    return position + action

### Possible outcomes of a generic game ###
class DWULT(Enum):
    DRAW = "Draw"
    WIN = "Win"
    UNKNOWN = "Unknown"
    LOSE = "Lose"
    TIE = "Tie"

### General solver ###
def solve(init_position, primitive, generate_moves, do_move):
    """
    Solves a game specified by the four inputs. Returns the
    result for the player starting at init_position, assuming
    optimal strategy. Assumes the game is a 2-player, perfect
    information, abstract strategy game.

    Currently only supports two results: 1. win 2. lose
    """
    # Cached positions, all of which is from the perspective of the current player
    # Maps (position) -> (win/lose, remoteness)
    solved_positions = {}

    # This function returns a (dwult, remoteness) tuple
    def solve_memoized(position, primitive, generate_moves, do_move, cache):
        # Return memoized soluton if it exists
        if position in cache:
            return cache[position]

        # Look at all possible next states
        next_moves = generate_moves(position)
        all_next_results = []
        for move in next_moves:
            next_pos = do_move(position, move)
            next_pos_results = solve_memoized(next_pos, primitive, generate_moves, do_move, cache)
            cache[next_pos] = next_pos_results
            all_next_results.append(next_pos_results)

        # Check that it's possible to force next player to lose
        result = DWULT.LOSE
        win_remoteness = float("inf")
        lose_remoteness = -float("inf")
        for next_result, remoteness in all_next_results:
            if next_result == DWULT.LOSE:
                result = DWULT.WIN
                # Win as fast as possible
                win_remoteness = min(win_remoteness, remoteness)
            else:
                # Lose as slow as possible
                lose_remoteness = max(lose_remoteness, remoteness)
        
        if result == DWULT.WIN:
            # No further moves from current game state
            if win_remoteness == float("inf"):
                win_remoteness = -1
            return result, win_remoteness + 1
        else:
            # No further moves from current game state
            if lose_remoteness == -float("inf"):
                lose_remoteness = -1
            return result, lose_remoteness + 1


    return solve_memoized(init_position, primitive, generate_moves, do_move, solved_positions)

def main():
    print(solve(init_position(), primitive, generate_moves, do_move))

if __name__ == "__main__":
    main()
