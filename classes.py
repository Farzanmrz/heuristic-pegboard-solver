# Imports
import copy

class State:

    def __init__(self, state=65023):
        """
        Initializes the State object.

        Args:
            state (int): Integer representation of the initial board state.
        """
        # Store integer representation of state
        self.state = state

        # Store binary representation of state
        self.binary_val = bin(self.state)[2:]

        # Store smallest integer 'n' required for a square grid by rooting the number of elements
        self.n = int(len(self.binary_val) ** 0.5)

        # Check if squaring the required length is less than current length
        if self.n ** 2 < len(self.binary_val):
            self.n += 1

        # Fill 0s in binary accordingly to complete n x n grid
        self.binary_val = self.binary_val.zfill(self.n ** 2)

        # Store the initial empty position for heuristic-based searches
        self.initial_empty = self.binary_val.find('0') if '0' in self.binary_val else None

    def __str__(self):
        """
        Converts the binary representation of the state into a readable grid.

        Returns:
            str: Grid representation of the state with 'X' for pegs and 'O' for empty slots.
        """
        # Convert to Xs and Os list to print
        xo_list = ['O' if bit == '0' else 'X' for bit in self.binary_val]

        # Return the grid layout, go through xo_list incrementing by n and adding linebreak
        return "\n".join(" ".join(xo_list[i:i + self.n]) for i in range(0, self.n ** 2, self.n))

    def goal_remaining(self):
        """
        Checks if the goal is achieved for flail-wildly (only one peg remains).

        Returns:
            bool: True if only one peg remains, False otherwise.
        """
        return self.binary_val.count('1') == 1

    def goal(self):
        """
        Checks if the goal is achieved for heuristic-based searches (one peg remains at the initial empty position).

        Returns:
            bool: True if only one peg remains and it's in the initial empty position, False otherwise.
        """
        return self.binary_val.count('1') == 1 and self.binary_val.find('1') == self.initial_empty

    def applicableActions(self):
        """
        Determines all valid actions for the current state.

        Returns:
            list: A list of valid actions, each represented as [jumper, goner, newpos].
        """
        # List to store actions
        actions = []

        # Loop through all combinations of jumper, goner, and new position
        for jumper in range(self.n ** 2):
            for goner in range(self.n ** 2):
                for newpos in range(self.n ** 2):

                    # If jumper = goner or any of the 3 equal to one another no point checking
                    if jumper != goner and jumper != newpos and goner != newpos:

                        # Make action object and check if precondition matches
                        action = Action([jumper, goner, newpos])
                        if action.precondition(self):
                            # If valid, add to actions list
                            actions.append([jumper, goner, newpos])

        return actions

class Action:
    """
    Represents an action in the pegboard game.

    An action consists of a jumper (the peg that moves), a goner (the peg that is removed),
    and a new position (where the jumper lands).
    """

    def __init__(self, actions):
        """
        Initialize the Action with a list containing values for jumper, goner and newpos.

        Args:
            actions (list): A list containing [jumper, goner, newpos] positions.
        """
        self.jumper = actions[0]
        self.goner = actions[1]
        self.newpos = actions[2]

    def __str__(self):
        """
        Define magic method to explain meaning of action.

        Returns:
            str: A readable string describing the action.
        """
        # Return readable string
        return ("The peg in slot " + str(self.jumper) +
                " jumps over the peg in slot " + str(self.goner) +
                " and lands in slot " + str(self.newpos))

    def applyState(self, state):
        """
        Apply the action to the current state and return the resulting new state.

        Args:
            state (State): The current state of the board.

        Returns:
            State: The new state after applying the action.
        """
        # Make deepcopy of state to return
        newState = copy.deepcopy(state)

        # Convert actions to integer values in binary for computation and set to state of new state
        newState.state = state.state + (2**self.newpos) - (2**self.jumper) - (
            2**self.goner)

        newState.binary_val = bin(newState.state)[2:]

        newState.binary_val = newState.binary_val.zfill(newState.n**2)

        # Return the new state
        return newState

    def precondition(self, state):
        """
        Check if the action is applicable to the given state.

        Args:
            state (State): The current state of the board.

        Returns:
            bool: True if the action is applicable, False otherwise.
        """
        # Convert to list for easier processing
        xo_list = [0 if bit == '0' else 1 for bit in state.binary_val]

        # Reverse the list to index easier because 0 index is position 15 right now
        xo_list.reverse()

        # Check if preconditions for jumper,goner and newpos are met
        if (xo_list[self.jumper] == 1 and xo_list[self.goner] == 1
                and xo_list[self.newpos] == 0):

            # Get 2D positions of jumper, goner and newpos
            jumper_pos = divmod(self.jumper, state.n)
            goner_pos = divmod(self.goner, state.n)
            newpos_pos = divmod(self.newpos, state.n)

            # Check horizontal alignment and consecutivity
            if (jumper_pos[0] == goner_pos[0] == newpos_pos[0]
                    and abs(jumper_pos[1] - goner_pos[1]) ==
                    abs(goner_pos[1] - newpos_pos[1]) == 1):
                return True

            # Check vertical alignment and consecutivity
            elif (jumper_pos[1] == goner_pos[1] == newpos_pos[1]
                  and abs(jumper_pos[0] - goner_pos[0]) ==
                  abs(goner_pos[0] - newpos_pos[0]) == 1):
                return True

            # Check diagonal alignment and consecutivity
            elif (abs(jumper_pos[0] - goner_pos[0]) ==
                  abs(jumper_pos[1] - goner_pos[1]) ==
                  abs(goner_pos[0] - newpos_pos[0]) ==
                  abs(goner_pos[1] - newpos_pos[1]) == 1
                  and jumper_pos[0] != newpos_pos[0]
                  and jumper_pos[1] != newpos_pos[1]):
                return True

        return False