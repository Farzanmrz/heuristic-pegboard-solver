# Imports
import importlib
import heuristics
import classes
importlib.reload(heuristics)
importlib.reload(classes)
from classes import State, Action
from heuristics import dfs, heuristic1, heuristic2, astar1, astar2, astar3
import random
import sys

def flailWildly(state):
    """
    Performs a random walk through the pegboard puzzle state space.

    This function randomly selects and applies valid actions to the current state
    until either a solution is found or no more actions are possible.

    Args:
        state (State): The initial state of the pegboard.

    Returns:
        None: Prints the steps taken and the result (success or failure).
    """
    # Print the current state
    print("***************************");
    print("Current state:\n" + str(state));

    # Get possible actions
    posActs = state.applicableActions()

    # If no actions remain print failure message and break
    if len(posActs) == 0:
        print("***************************")
        print("Sorry better luck next time")
        return

    # Get random action by modulus of id with actions length
    currAct = posActs[random.randint(0,
                                     len(posActs) - 1)]

    # Print the action being applied
    print("Action chosen: " + str(currAct))

    # Create action object with the action chosen
    newAct = Action(currAct)

    # Apply to current state
    newState = newAct.applyState(state)

    # Check if goal state
    if newState.goal_remaining():

        # Print success message, success state and break
        print("***************************")
        print("Congratulations solved! Final state:")
        print(str(newState))
        return

    # Recursively enter same function to keep running
    flailWildly(newState)

if __name__ == "__main__":

    # Check if valid number of input arguments
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <function> <state>")
        sys.exit(1)

    # Store the function and state parameters
    func = sys.argv[1]
    state = sys.argv[2]

    # Check if state is passed as an int
    try:
        initial_state = int(state)
    except ValueError:
        print("Error: <state> must be an integer.")
        sys.exit(1)

    # Create the initial state object
    initial_state = State(initial_state)

    # Handle the requested function
    if func == "flailWildly":
        flailWildly(initial_state)
    elif func == "dfs":
        dfs(initial_state)
    elif func == "heuristic1":
        print(f"Heuristic1 Value: {heuristic1(initial_state)}")
    elif func == "heuristic2":
        print(f"Heuristic2 Value: {heuristic2(initial_state)}")
    elif func == "astar1":
        astar1(initial_state)
    elif func == "astar2":
        astar2(initial_state)
    elif func == "astar3":
        astar3(initial_state)
    else:
        print(f"Unknown function: {func}")
        print(
            "Available functions: flailWildly, dfs, heuristic1, heuristic2, astar1, astar2, astar3"
        )
        sys.exit(1)