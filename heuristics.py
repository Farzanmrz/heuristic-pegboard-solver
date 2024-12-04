import importlib
import classes
importlib.reload(classes)
from classes import Action
import time
import heapq
import itertools

def dfs(state):
    """
    Performs a Depth-First Search to find a solution for the pegboard puzzle.

    Args:
        state (State): The initial state of the pegboard.

    Returns:
        None: Prints the solution path and statistics if found, or a failure message.
    """
    # Define stack to store current state integer and path as list storing (action, state)
    stack = [(state, [(None, state)])]

    # Keep a set of closed nodes
    closed = set()

    # Keep track of expanded nodes
    nodes = 0

    # Store starting time
    start = time.time()

    # While the stack is not empty
    while stack:

        # Set the current state and path to the last in element of stack
        currState, path = stack.pop()

        # Add the integer representation of current state to set of closed nodes
        closed.add(currState.state)

        # If the current state is goal then
        if currState.goal():

            # Store the end time when goal state was found
            end = time.time()

            # Print success message and number of expanded nodes
            print("Congratulations solved!")
            print("Expanded Nodes: " + str(nodes))

            # Extract actions from the path tuple in a list and print
            solution_path = [
                action for action, _ in path if action is not None
            ]
            print("Solution Path: " +
                  ' -> '.join([str(action) for action in solution_path]))

            # Calculate total time and print
            print("Total Time Elapsed: {:.2f} seconds".format(end - start))
            print("\n")

            # Iterate through the path printing the action and the resultant state stored in path
            for action, state in path:

                # Skip first iteration where action is none
                if action is not None:

                    # Print the action
                    print(f"Action: {action}")

                # Print the state
                print(f"State:\n{state}\n")

            # Return nothing since we just have to print output
            return None

        # Iterate through all the applicable actions
        for currAct in currState.applicableActions():

            # Create action object with the action chosen
            newAct = Action(currAct)

            # Apply to current state
            newState = newAct.applyState(currState)

            # Only visit the new state if it has not been closed
            if newState.state not in closed:

                # Increment the number of nodes
                nodes += 1

                # Generate a new path adding the current action and newstate
                newPath = path + [(currAct, newState)]

                # Append it to the stack
                stack.append((newState, newPath))

    # Store the end time if no goal state was found
    end = time.time()

    # Print failure message and number of expanded nodes
    print("Sorry better luck next time")
    print("Expanded Nodes: " + str(nodes))

    # Calculate total time and print
    print("Total Time Elapsed: {:.2f} seconds".format(end - start))

    # Return nothing since we just have to print output
    return None

def heuristic1(state):
    """
    Heuristic function that returns the number of applicable actions.

    Args:
        state (State): The current state of the pegboard.

    Returns:
        int: The number of applicable actions for the given state.
    """
    return len(state.applicableActions())

def heuristic2(state):
    """
    Heuristic function that returns the sum of the Manhattan distances.

    Args:
        state (State): The current state of the pegboard.

    Returns:
        int: The sum of Manhattan distances from each peg to the initial empty position.
    """
    # Check if there is no initial_empty position
    if state.initial_empty is None:
        return 0

    # Convert initial empty position to 2D coordinates
    empty_x, empty_y = divmod(state.initial_empty, state.n)

    # Variable for total distance
    distance = 0

    # Iterate through the binary
    for i, bit in enumerate(state.binary_val):

        # If X is found then
        if bit == '1':

            # Convert to 2D
            x, y = divmod(i, state.n)

            # Get manhattan distance from initial empty position and add to distance
            distance += abs(x - empty_x) + abs(y - empty_y)

    return distance

def astar1(state):
    """
    Performs A* search using heuristic1 to find a solution for the pegboard puzzle.

    Args:
        state (State): The initial state of the pegboard.

    Returns:
        None: Prints the solution path and statistics if found, or a failure message.
    """
    # Unique counter for each item in the priority queue for tie-breaker
    counter = itertools.count()

    # Store nodes to be opened in priority queue
    open_nodes = []

    # Store the current heuristic value, counter and the current state object
    heapq.heappush(open_nodes, (heuristic1(state), next(counter), state))

    # Create set to track states in priority queue
    open_nodes_states = {state.state}

    # Store lowest g(n) and f(n) in sets for each state initially g(n) = 0
    g_n = {state.state: 0}
    f_n = {state.state: heuristic1(state)}

    # Maps each node to the node/state it was reached from
    prevNode = {}

    # Maps each node to the action that was taken to reach it from previous node/state
    prevAct = {}

    # Keep track of expanded nodes
    nodes = 0

    # Store starting time
    start = time.time()

    # Loop while there are nodes in open list
    while open_nodes:

        # Get current state with lowest f(n)
        _, _, currState = heapq.heappop(open_nodes)

        # Removes from set of open nodes being tracked
        open_nodes_states.remove(currState.state)

        # Check if current state is goal
        if currState.goal():

            # Store the end time when goal state was found
            end = time.time()

            # Get the path
            path = []

            # Loop till currState has an entry in prevNode
            while currState in prevNode:

                # Retreive the action that led to the current state
                currAct = prevAct[currState]

                # Add the action taken and the current state to path
                path.append((currAct, currState))

                # Move one step backward and set current state to the previous state
                currState = prevNode[currState]

            # Reverse the reconstructed path for proper chronological order
            path.reverse()

            # Print success message and the number of expanded nodes
            print("Congratulations solved!")
            print(f"Expanded Nodes: " + str(nodes))

            # Extract actions from the path tuple in a list and print
            solution_path = [
                action for action, _ in path if action is not None
            ]
            print("Solution Path: " +
                  ' -> '.join([str(action) for action in solution_path]))

            # Calculate total time and print
            print("Total Time Elapsed: {:.2f} seconds".format(end - start))
            print("\n")

            # Print initial state
            print(f"State:\n{state}\n")

            # Iterate through the path printing the action and the resultant state stored in path
            for action, state in path:
                if action is not None:
                    print(f"Action: {action}")
                print(f"State:\n{state}\n")

            # Return nothing since we just have to print output
            return None

        # Iterate through all applicable actions
        for currAct in currState.applicableActions():

            # Create action object with the action chosen
            newAct = Action(currAct)

            # Apply to current state to get new state
            newState = newAct.applyState(currState)

            # Check if the current g(n) is less than the previous g(n) for this newState
            # If this newState is not in the g_n dictionary yet then just compare with infinity
            if (g_n[currState.state] + 1) < (g_n.get(newState.state,
                                                     float('inf'))):

                # If current g(n) is lesser than the previous one then this path is better
                # Update the previous node to this newState as the current state
                prevNode[newState] = currState

                # Update the previous action to store this current action
                prevAct[newState] = currAct

                # Update the g(n) to store the current g(n) value
                g_n[newState.state] = g_n[currState.state] + 1

                # Update the f(n) to store the current f(n) value computed with new g(n)
                f_n[newState.
                    state] = g_n[newState.state] + heuristic1(newState)

                # If the newState is not in open_nodes_states then add to priority queue
                if newState.state not in open_nodes_states:

                    # Push to the priority queue
                    heapq.heappush(
                        open_nodes,
                        (f_n[newState.state], next(counter), newState))

                    # Add to the set of open node states
                    open_nodes_states.add(newState.state)

                    # Increment the number of nodes expanded
                    nodes += 1

    # Store the end time if no goal state was found
    end = time.time()

    # Print failure message and number of expanded nodes
    print("Sorry better luck next time")
    print("Expanded Nodes: " + str(nodes))

    # Calculate total time and print
    print("Total Time Elapsed: {:.2f} seconds".format(end - start))

    # Return nothing since we just have to print output
    return None

def astar2(state):
    """
    Performs A* search using heuristic2 to find a solution for the pegboard puzzle.

    Args:
        state (State): The initial state of the pegboard.

    Returns:
        None: Prints the solution path and statistics if found, or a failure message.
    """
    # Unique counter for each item in the priority queue for tie-breaker
    counter = itertools.count()

    # Store nodes to be opened in priority queue
    open_nodes = []

    # Store the current heuristic value, counter and the current state object
    heapq.heappush(open_nodes, (heuristic2(state), next(counter), state))

    # Create set to track states in priority queue
    open_nodes_states = {state.state}

    # Store lowest g(n) and f(n) in sets for each state initially g(n) = 0
    g_n = {state.state: 0}
    f_n = {state.state: heuristic2(state)}

    # Maps each node to the node/state it was reached from
    prevNode = {}

    # Maps each node to the action that was taken to reach it from previous node/state
    prevAct = {}

    # Keep track of expanded nodes
    nodes = 0

    # Store starting time
    start = time.time()

    # Loop while there are nodes in open list
    while open_nodes:

        # Get current state with lowest f(n)
        _, _, currState = heapq.heappop(open_nodes)

        # Removes from set of open nodes being tracked
        open_nodes_states.remove(currState.state)

        # Check if current state is goal
        if currState.goal():

            # Store the end time when goal state was found
            end = time.time()

            # Get the path
            path = []

            # Loop till currState has an entry in prevNode
            while currState in prevNode:

                # Retreive the action that led to the current state
                currAct = prevAct[currState]

                # Add the action taken and the current state to path
                path.append((currAct, currState))

                # Move one step backward and set current state to the previous state
                currState = prevNode[currState]

            # Reverse the reconstructed path for proper chronological order
            path.reverse()

            # Print success message and the number of expanded nodes
            print("Congratulations solved!")
            print(f"Expanded Nodes: " + str(nodes))

            # Extract actions from the path tuple in a list and print
            solution_path = [
                action for action, _ in path if action is not None
            ]
            print("Solution Path: " +
                  ' -> '.join([str(action) for action in solution_path]))

            # Calculate total time and print
            print("Total Time Elapsed: {:.2f} seconds".format(end - start))
            print("\n")

            # Print initial state
            print(f"State:\n{state}\n")

            # Iterate through the path printing the action and the resultant state stored in path
            for action, state in path:
                if action is not None:
                    print(f"Action: {action}")
                print(f"State:\n{state}\n")

            # Return nothing since we just have to print output
            return None

        # Iterate through all applicable actions
        for currAct in currState.applicableActions():

            # Create action object with the action chosen
            newAct = Action(currAct)

            # Apply to current state to get new state
            newState = newAct.applyState(currState)

            # Check if the current g(n) is less than the previous g(n) for this newState
            # If this newState is not in the g_n dictionary yet then just compare with infinity
            if (g_n[currState.state] + 1) < (g_n.get(newState.state,
                                                     float('inf'))):

                # If current g(n) is lesser than the previous one then this path is better
                # Update the previous node to this newState as the current state
                prevNode[newState] = currState

                # Update the previous action to store this current action
                prevAct[newState] = currAct

                # Update the g(n) to store the current g(n) value
                g_n[newState.state] = g_n[currState.state] + 1

                # Update the f(n) to store the current f(n) value computed with new g(n)
                f_n[newState.
                    state] = g_n[newState.state] + heuristic2(newState)

                # If the newState is not in open_nodes_states then add to priority queue
                if newState.state not in open_nodes_states:

                    # Push to the priority queue
                    heapq.heappush(
                        open_nodes,
                        (f_n[newState.state], next(counter), newState))

                    # Add to the set of open node states
                    open_nodes_states.add(newState.state)

                    # Increment the number of nodes expanded
                    nodes += 1

    # Store the end time if no goal state was found
    end = time.time()

    # Print failure message and number of expanded nodes
    print("Sorry better luck next time")
    print("Expanded Nodes: " + str(nodes))

    # Calculate total time and print
    print("Total Time Elapsed: {:.2f} seconds".format(end - start))

    # Return nothing since we just have to print output
    return None

def heuristic3(state):
    """
    An improved heuristic function that combines the number of pegs with manhattan distance.

    Args:
        state (State): The current state of the pegboard.

    Returns:
        int: The heuristic value for the given state.
    """
    # Weight factor got via trial and error more pegs is less desirable state
    weight = 3

    # Count the number of pegs with Xs in them
    pegs = bin(int(state.binary_val, 2)).count('1')

    # Add the weighted score of number of pegs with the manhattan distance
    return (pegs * weight) + heuristic2(state)

def astar3(state):
    """
    Performs A* search using the improved heuristic3 to find a solution for the pegboard puzzle.

    Args:
        state (State): The initial state of the pegboard.

    Returns:
        None: Prints the solution path and statistics if found, or a failure message.
    """
    # Unique counter for each item in the priority queue for tie-breaker
    counter = itertools.count()

    # Store nodes to be opened in priority queue
    open_nodes = []

    # Store the current heuristic value, counter and the current state object
    heapq.heappush(open_nodes, (heuristic3(state), next(counter), state))

    # Create set to track states in priority queue
    open_nodes_states = {state.state}

    # Store lowest g(n) and f(n) in sets for each state initially g(n) = 0
    g_n = {state.state: 0}
    f_n = {state.state: heuristic3(state)}

    # Maps each node to the node/state it was reached from
    prevNode = {}

    # Maps each node to the action that was taken to reach it from previous node/state
    prevAct = {}

    # Keep track of expanded nodes
    nodes = 0

    # Store starting time
    start = time.time()

    # Loop while there are nodes in open list
    while open_nodes:

        # Get current state with lowest f(n)
        _, _, currState = heapq.heappop(open_nodes)

        # Removes from set of open nodes being tracked
        open_nodes_states.remove(currState.state)

        # Check if current state is goal
        if currState.goal():

            # Store the end time when goal state was found
            end = time.time()

            # Get the path
            path = []

            # Loop till currState has an entry in prevNode
            while currState in prevNode:

                # Retreive the action that led to the current state
                currAct = prevAct[currState]

                # Add the action taken and the current state to path
                path.append((currAct, currState))

                # Move one step backward and set current state to the previous state
                currState = prevNode[currState]

            # Reverse the reconstructed path for proper chronological order
            path.reverse()

            # Print success message and the number of expanded nodes
            print("Congratulations solved!")
            print(f"Expanded Nodes: " + str(nodes))

            # Extract actions from the path tuple in a list and print
            solution_path = [
                action for action, _ in path if action is not None
            ]
            print("Solution Path: " +
                  ' -> '.join([str(action) for action in solution_path]))

            # Calculate total time and print
            print("Total Time Elapsed: {:.2f} seconds".format(end - start))
            print("\n")

            # Print initial state
            print(f"State:\n{state}\n")

            # Iterate through the path printing the action and the resultant state stored in path
            for action, state in path:
                if action is not None:
                    print(f"Action: {action}")
                print(f"State:\n{state}\n")

            # Return nothing since we just have to print output
            return None

        # Iterate through all applicable actions
        for currAct in currState.applicableActions():

            # Create action object with the action chosen
            newAct = Action(currAct)

            # Apply to current state to get new state
            newState = newAct.applyState(currState)

            # Check if the current g(n) is less than the previous g(n) for this newState
            # If this newState is not in the g_n dictionary yet then just compare with infinity
            if (g_n[currState.state] + 1) < (g_n.get(newState.state,
                                                     float('inf'))):

                # If current g(n) is lesser than the previous one then this path is better
                # Update the previous node to this newState as the current state
                prevNode[newState] = currState

                # Update the previous action to store this current action
                prevAct[newState] = currAct

                # Update the g(n) to store the current g(n) value
                g_n[newState.state] = g_n[currState.state] + 1

                # Update the f(n) to store the current f(n) value computed with new g(n)
                f_n[newState.
                    state] = g_n[newState.state] + heuristic3(newState)

                # If the newState is not in open_nodes_states then add to priority queue
                if newState.state not in open_nodes_states:

                    # Push to the priority queue
                    heapq.heappush(
                        open_nodes,
                        (f_n[newState.state], next(counter), newState))

                    # Add to the set of open node states
                    open_nodes_states.add(newState.state)

                    # Increment the number of nodes expanded
                    nodes += 1

    # Store the end time if no goal state was found
    end = time.time()

    # Print failure message and number of expanded nodes
    print("Sorry better luck next time")
    print("Expanded Nodes: " + str(nodes))

    # Calculate total time and print
    print("Total Time Elapsed: {:.2f} seconds".format(end - start))

    # Return nothing since we just have to print output
    return None
