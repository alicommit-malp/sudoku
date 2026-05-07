import random
import numpy as np

class PuzzleGenerator:
    def __init__(self):
        pass

    # Helper to check whether a number can be placed in a given cell
    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        box_row_start = row - row % 3
        box_col_start = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + box_row_start][j + box_col_start] == num:
                    return False
        return True

    # Recursive backtracking to fill the grid
    def fill_grid(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    num_list = list(range(1, 10))
                    random.shuffle(num_list)
                    for num in num_list:
                        if self.is_valid(grid, i, j, num):
                            grid[i][j] = num
                            if self.fill_grid(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True

    # Count solutions, capped at `cap`. The default cap=2 is enough for the
    # uniqueness check below — going higher would just enumerate solutions we
    # never use, and is meaningfully slower on under-constrained puzzles.
    def count_solutions(self, grid, cap=2):
        count = [0]
        self._solve(grid.copy(), count, cap)
        return count[0]

    def _solve(self, grid, count, cap):
        if count[0] >= cap:
            return
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(grid, i, j, num):
                            grid[i][j] = num
                            self._solve(grid, count, cap)
                            grid[i][j] = 0
                            if count[0] >= cap:
                                return
                    return
        count[0] += 1

    def has_unique_solution(self, grid):
        return self.count_solutions(grid) == 1

    # Generate a full Sudoku grid and remove numbers based on min_clues
    def generate_sudoku(self, min_clues=30):
        grid = np.zeros((9, 9), dtype=int)
        self.fill_grid(grid)  # Create a full valid grid

        # Remove numbers to match the exact number of clues requested (e.g., 17 for min_clues=17)
        puzzle = self.remove_numbers_exact_clues(grid.copy(), num_clues=min_clues)
        return puzzle, grid

    # Remove numbers to leave exactly num_clues in the grid
    def remove_numbers_exact_clues(self, grid, num_clues):
        total_cells = 81
        cells_to_remove = total_cells - num_clues  # We want to remove this many cells
        removed = 0

        all_cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(all_cells)

        for row, col in all_cells:
            if removed >= cells_to_remove:
                break

            if grid[row][col] == 0:
                continue

            backup = grid[row][col]
            grid[row][col] = 0

            # Check if the puzzle still has a unique solution
            if self.has_unique_solution(grid):
                removed += 1  # Successful removal
            else:
                grid[row][col] = backup  # Restore if removing breaks uniqueness

        return grid
