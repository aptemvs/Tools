from itertools import product

# Define the Sudoku grid size
SIZE = 4
BLOCK_SIZE = 2

# The given Sudoku grid (using 0 for empty cells)
grid = [
    [0, 0, 4, 0],
    [0, 1, 0, 3],
    [0, 2, 0, 0],
    [0, 0, 0, 0]
]


# Function to generate the Boolean variables
def var(r, c, v):
    """
    r - row
    c - column
    v - value (1 or 2 or 3 or 4)

    r + 1 and c + 1 to make output user understandable: numeration from 1, not 0
    """
    return f"c_{r + 1}{c + 1}{v}"


# Generate the cell constraints
def cell_constraints():
    """
    This function ensures that at least one value will be in the cell
    """
    constraints = []
    for r, c in product(range(SIZE), range(SIZE)):
        constraints.append(f"({' | '.join(var(r, c, v) for v in range(1, SIZE + 1))})")
    return ' & '.join(constraints)


# Generate the row constraints
def row_constraints():
    """
    This function ensures that row condition for each row is met: there shouldn't be two equal numbers in one row
    """

    constraints = []
    for v in range(1, SIZE + 1):
        for c in range(SIZE):
            constraints.append(f"({' | '.join(var(r, c, v) for r in range(SIZE))})")
            for r1, r2 in product(range(SIZE), range(SIZE)):
                if r1 < r2:
                    constraints.append(f"~({var(r1, c, v)} & {var(r2, c, v)})")
    return ' & '.join(constraints)


def col_constraints():
    """
    This function ensures that col condition for each col is met: there shouldn't be two equal numbers in one col
    """

    constraints = []
    for v in range(1, SIZE + 1):
        for r in range(SIZE):
            constraints.append(f"({' | '.join(var(r, c, v) for c in range(SIZE))})")
            for c1, c2 in product(range(SIZE), range(SIZE)):
                if c1 < c2:
                    constraints.append(f"~({var(r, c1, v)} & {var(r, c2, v)})")

    return ' & '.join(constraints)


# Generate the block constraints
def block_constraints():
    """
    This function checks that:
     1. Each number should be in "subbloc" of sudoku at least once
     2. Each number shouldn't be in "subblock" of sudoku more than once
    """
    constraints = []
    for v in range(1, SIZE + 1):
        for br in range(0, SIZE, BLOCK_SIZE):
            for bc in range(0, SIZE, BLOCK_SIZE):
                # Generate variables for each block
                block_cells = [var(r, c, v)
                               for r in range(br, br + BLOCK_SIZE)
                               for c in range(bc, bc + BLOCK_SIZE)]
                # Constraint to ensure each number appears at least once in each block
                constraints.append(f"({' | '.join(block_cells)})")
                # Constraints to ensure each number appears at most once in each block
                for i, cell1 in enumerate(block_cells):
                    for cell2 in block_cells[i + 1:]:
                        constraints.append(f"~({cell1} & {cell2})")
    return ' & '.join(constraints)


# Generate constraints for initial task values
def prefilled_constraints(grid):
    constraints = []
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value:
                constraints.append(var(r, c, value))
    return ' & '.join(constraints)


# Combine all constraints
def generate_formula(grid):
    formula = []
    formula.append(cell_constraints())
    formula.append(row_constraints())
    formula.append(col_constraints())
    formula.append(block_constraints())
    formula.append(prefilled_constraints(grid))
    return ' & '.join(formula)


# Generate the formula
sudoku_formula = generate_formula(grid)

# Output the formula
print(sudoku_formula)
