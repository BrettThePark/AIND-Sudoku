assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Add the contraints needed to enforce diagonal Sudoku
# Build two array elements with the top left to lower right and
# bottom left to top right diagonal
diagonal_units = [[r+c for (r,c) in zip(list(rows), list(cols))],
         [r+c for (r,c) in zip(list(rows), list(reversed(list(cols))))]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unitGroups in units.values():
        for group in unitGroups:
            for box in group:
                boxValue = values[box]
                # For each box in group find identical values
                boxesWithSameValue = [b for b in group if values[b] == boxValue]
                # If we find more the same number of boxes as value character
                # count (and more than 1) we have found a naked_grouping
                # twins, triplet, quadrouplets, etc. 
                if len(boxesWithSameValue) > 1 and len(boxesWithSameValue) == len(boxValue):
                    for boxToRemoveTwins in group:
                        if boxToRemoveTwins not in boxesWithSameValue:
                            newValue = values[boxToRemoveTwins].translate({ord(c):None for c in list(boxValue)})
                            assign_value(values, boxToRemoveTwins, newValue)
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81
    values = dict(zip(boxes,grid))
    for box,boxValue in values.items():
        if boxValue == '.':
            values[box] = '123456789'
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # Straight from the lesson
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """
    Eliminate values that are not valid due to already being used
    in a peer box
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the already solved values
        eliminated from peers.
    """
    for box, boxValue in values.items():
        if len(boxValue) == 1:
            # Find all boxes to remove from known value from
            for boxToClean in peers[box]:
                newValue = values[boxToClean].replace(boxValue, '')
                assign_value(values, boxToClean, newValue)
    return values

def only_choice(values):
    """
    Look through each unit and decide if there is only one possible solution
    for a particular digit
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with only choice decisions resolved.
    """
    for box, unitGroups in units.items():
        for unit in unitGroups:
            # For each unit create a list of all the possible digits
            unitString = ''.join([values[k] for k in unit])
            boxValues = values[box]
            # For each digit in the box, check to see if it only occurs
            # once in the whole unit. If so, we have the only choice
            for boxValue in boxValues:
                if unitString.count(boxValue) == 1:
                    assign_value(values, box, boxValue)
                    break
    return values

def reduce_puzzle(values):
    """
    Continously run a series of constraint solving methods until the puzzle
    can no longer be reduced. Largely from the lessons.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary that is as fully reduced as possible using
        constraints
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        eliminate(values)
        # Use the Only Choice Strategy
        only_choice(values)
        # Use the Naked Twins Strategy
        naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Using depth-first search and propagation, 
    create a search tree and solve the sudoku.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        False in the case of no solution. Otherwise a fully solved sudoku
        puzzle as a values dictionary
    """
    ""
    # First, reduce the puzzle using the previous function
    partialSolve = reduce_puzzle(values)
    
    #Check if it solved
    if partialSolve is False:
        return partialSolve
    elif len([box for box in partialSolve.keys() if len(values[box]) != 1]) == 0:
        return partialSolve
    
    # Create a list of unsolved boxes ordered by least number of 
    # possibilities in order to reduce search space
    sortedBoxes = [key for key in sorted(values, key=lambda k: len(values[k])) if len(partialSolve[key]) > 1]
    # Use the smallest box
    minBox = sortedBoxes[0]
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for branch in partialSolve[minBox]:
        optimisticValues = partialSolve.copy()
        assign_value(optimisticValues, minBox, branch)
        # Recursive call for searching
        result = search(optimisticValues)
        if result:
            return result

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # Convert into a dictionary
    dictGrid = grid_values(grid)
    # Perform the constraint solving and search techniques to solve
    dictGrid = search(dictGrid)
    return dictGrid

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
