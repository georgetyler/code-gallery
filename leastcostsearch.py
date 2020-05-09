# See leastcostsearch.md for detailed specification.
# Script contains four functions:
# build_cave creates a representation of a graph according to fixed and variable parameters.
# check_path checks if a given path through the graph satisfies certain rules
# shortest_path implements a breadth-first search algorithm for the shortest path through the graph
# optimal_path implements a least-cost search with a priority queue for the optimal path through the graph.


# ** BUILD CAVE FUNCTION
def build_cave(data):
    """ Build a 2D representation of a cave from a given dictionary.
    :param data: dict
    :return: int
    """

    # Initialise an empty cave
    global dragon_col
    row = []
    cave = []
    for i in range(data['size']):
        row.append('.')

    for i in range(data['size']):
        row = list(row)  # Creates independently mutable rows
        cave.append(row)

    # Add entrance
    # Check for existence of single entrance and add

    if 'entrance' in data:
        entrance_row = data['entrance'][0]
        entrance_col = data['entrance'][1]

        cave[entrance_row][entrance_col] = '@'

    else:
        return None

    # Add exit
    # Check for existence of a single exit
    # Check if it is overwriting an existing feature: if so, cave invalid
    if 'exit' in data:
        exit_row = data['exit'][0]
        exit_col = data['exit'][1]
        if cave[exit_row][exit_col] == '.':
            cave[exit_row][exit_col] = 'X'
        else:
            return None
    else:
        return None

    # Add dragon
    if 'dragon' in data:
        dragon_row = data['dragon'][0]
        dragon_col = data['dragon'][1]

        # Add to cave with overwriting check
        if cave[dragon_row][dragon_col] == '.':
            cave[dragon_row][dragon_col] = 'W'
        else:
            return None

    # Add sword
    if 'sword' in data:
        sword_row = data['sword'][0]
        sword_col = data['sword'][1]

        # Add to cave with overwriting check
        if cave[sword_row][sword_col] == '.':
            cave[sword_row][sword_col] = 't'

        else:
            return None

    # Add treasure(s)
    if 'treasure' in data:
        if len(data['treasure']) <= 3:
            for location in data['treasure']:
                treasure_row = location[0]
                treasure_col = location[1]

                # Add to cave with overwriting check
                if cave[treasure_row][treasure_col] == '.':
                    cave[treasure_row][treasure_col] = '$'
                else:
                    return None
        else:
            return None

    # Add walls
    if 'walls' in data:

        for i in data['walls']:
            wall_row = i[0]
            wall_col = i[1]

            # Add to cave with overwriting check
            if cave[wall_row][wall_col] == '.':
                cave[wall_row][wall_col] = '#'
            else:
                return None

    # Finally, check if the dragon is adjacent to the entrance
    # This is the case if it occupies both an adjacent row and an adjacent col
    if 'dragon' in data:
        if entrance_col in range(dragon_col - 1, dragon_col + 1):
            if entrance_row in range(dragon_row - 1, dragon_row + 1):
                return None

    return cave


# ** CHECK PATH FUNCTION
def check_path(data, path):
    """ Checks validity of a given path against criteria. Returns bool.

    """
    # Create ordered list of tuples corresponding to the locations Falca visits
    locations = []
    currloc = data['entrance']
    locations.append(currloc)
    for i in path:
        if i == 'N':
            currloc = (currloc[0] - 1, currloc[1])

        if i == 'S':
            currloc = (currloc[0] + 1, currloc[1])

        if i == 'E':
            currloc = (currloc[0], currloc[1] + 1)

        if i == 'W':
            currloc = (currloc[0], currloc[1] - 1)

        locations.append(currloc)

    # Commence list of checks; if none return false then path is valid

    # 1. Check that Falca never visits an out-of-bounds square
    for location in locations:
        for coordinate in location:
            if (coordinate > data['size']) or (coordinate < 0):
                return False

    # 2. Check that Falca never occupies a wall square
    if 'walls' in data:
        for location in locations:
            for wall in data['walls']:
                if location == wall:
                    return False

    # 3. Check that Falca occupies dragon-adjacent square only after occupying
    # the sword square:

    # Build list of dragon-adjacent squares
    if 'dragon' in data:
        dragon_row = data['dragon'][0]
        dragon_col = data['dragon'][1]
        dragon_squares = []
        sword_location = data['sword']
        obtained_sword = False

        for row in range(dragon_row - 1, dragon_row + 2):
            for col in range(dragon_col - 1, dragon_col + 2):
                dragon_squares.append((row, col))

        # Check location sequence to verify sword found _before_ dragon
        for location in locations:
            if location == sword_location:
                obtained_sword = True

            if (location in dragon_squares) and not obtained_sword:
                return False

    # 4. Check that all treasures have been visited
    treasure_squares = data['treasure']
    for chest in treasure_squares:
        for _ in locations:
            if chest not in locations:
                return False

    # 5. Check that Falca's final square is the exit square
    if locations[-1] != data['exit']:
        return False

    return True


# ** SHORTEST PATH FUNCTION
def shortest_path(data, start, end, has_sword):
    ''' Evaluate length of shortest path from a specified start and end point.
    Returns integer (path length) or None (no path exists).

    '''
    # Create list of occupied squares
    wall_squares = []
    for i in data['walls']:
        wall_squares.append(i)

    # Create list of dragon-adjacent squares
    dragon_row = data['dragon'][0]
    dragon_col = data['dragon'][1]
    dragon_squares = []

    for row in range(dragon_row - 1, dragon_row + 2):
        for col in range(dragon_col - 1, dragon_col + 2):
            dragon_squares.append((row, col))

    # Breadth-first search with depth marker for length of longest branch
    depth = 0
    node = [start, depth]
    unexplored = [node]
    explored = []

    while unexplored:

        # Extract node location and its depth, incrementing depth if necessary
        node, unexplored_depth = unexplored.pop(0)

        if unexplored_depth > depth:
            depth += 1

        if node == end:
            return depth

        explored.append(node)

        # Generate list of potential moves in all 4 directions

        potential_moves = [(node[0] - 1, node[1]), (node[0] + 1, node[1]), (node[0], node[1] + 1),
                           (node[0], node[1] - 1)]

        # Eliminate invalid moves in this list using a boolean w/ tests
        valid_moves = []

        for move in potential_moves:

            is_valid = True

            # If it's already explored or in queue: mark invalid
            if move in explored:
                is_valid = False

            if move in unexplored:
                is_valid = False

            # Out of bounds / dragon / wall checks:

            for i in move:
                if (i < 0) or (i > data['size'] - 1):
                    is_valid = False

            if (move in dragon_squares) and not has_sword:
                is_valid = False

            if move in wall_squares:
                is_valid = False

            # If candidate move survives checks, add to list of valid moves
            if is_valid:
                valid_moves.append(move)

        # Finally, add remaining valid moves to queue
        # Depth is incremented for all children, allowing for multiple branches

        for child in valid_moves:
            unexplored.append([child, depth + 1])


# ** OPTIMAL PATH FUNCTION
def optimal_path(data):
    '''Find length of the shortest path that enables Falca to collect
    all treasures and exit the dungeon.
    Returns integer (path length) or None (no path exists).
    '''
    node = (0, data['entrance'])  # Nodes are tuples with the cumulative cost
    unexplored = [node]  # Priority queue
    explored = []
    money_found = False  # Makes exit node available after all treasure found
    has_sword = False  # Removes dragon obstacle when calling shortest_path

    while unexplored:

        # First retrieve the node with the next-cheapest path & add to explored
        unexplored = sorted(unexplored)
        node = unexplored.pop(0)
        explored.append(node)

        # If goal state reached, we have the cheapest solution, so return cost
        if node[1] == data['exit']:
            return node[0]

        valid_moves = []

        # If path exists to a treasure location, add it to valid moves
        if 'treasure' in data:
            for i in data['treasure']:
                if shortest_path(data, node[1], i, has_sword):
                    valid_moves.append(i)

        # Compare explored locations with treasure locations to determine if
        # all money has been found
        treasures_visited = 0
        for i in explored:
            if 'treasure' in data:
                if i[1] in data['treasure']:
                    treasures_visited += 1

        if 'treasure' in data:
            if treasures_visited == len(data['treasure']):
                money_found = True

        # If all the treasure has been found, add exit node
        if shortest_path(data, node[1], data['exit'], has_sword):
            if money_found:
                valid_moves.append(data['exit'])

        # Add sword node
        if shortest_path(data, node[1], data['sword'], has_sword):
            valid_moves.append(data['sword'])

        # Finally, evaluate valid moves
        for move in valid_moves:

            # Add the cost to the move to get the child
            cost = node[0] + shortest_path(data, node[1], move, has_sword)
            child = (cost, move)

            # Determine whether the child is already explored or in queue
            child_in_unexplored = False
            for location in unexplored:
                if location[1] == child[1]:
                    child_in_unexplored = True

            child_in_explored = False
            for location in explored:
                if location[1] == child[1]:
                    child_in_explored = True

            # If it's totally new, add it to the queue
            if not child_in_unexplored:
                if not child_in_explored:
                    if child[1] == data['sword']:
                        has_sword = True  # Flip switch if sword picked up

                    unexplored.append(child)

            # If it's in the queue but a smaller cost, replace
            elif child_in_unexplored:
                for location in unexplored:
                    if location[1] == child[1] and child[0] < location[0]:
                        unexplored.remove(location)
                        unexplored.append(child)
