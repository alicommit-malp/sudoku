import random
import numpy as np

from puzzle_generator import PuzzleGenerator

class AdvancedSudokuGenerator(PuzzleGenerator):

    def generate_professional_sudoku(self, min_clues=30, symmetry=False):
        grid = np.zeros((9, 9), dtype=int)
        self.fill_grid(grid)  # Create a fully solved grid
        solution = grid.copy()

        if symmetry:
            puzzle = self.remove_numbers_with_symmetry(grid.copy(), num_clues=min_clues)
        else:
            puzzle = self.remove_numbers_exact_clues(grid.copy(), num_clues=min_clues)

        # Note: we do not force the puzzle to *exactly* `min_clues`. Forcing it
        # would require either restoring givens (no harm) or removing more cells
        # without a uniqueness check (which silently produces ambiguous puzzles).
        # `min_clues` is treated as a target lower bound; the achieved count may
        # be higher when uniqueness-preserving removal cannot continue. Symmetric
        # removal in particular often settles well above the target.
        return puzzle, solution

    def remove_numbers_with_symmetry(self, grid, num_clues):
        cells_to_remove = 81 - num_clues
        removed = 0

        # Representatives of each 180°-rotational pair. The center cell (4, 4)
        # is its own pair and must be counted as a single cell, not two.
        symmetric_pairs = [
            (r, c, 8 - r, 8 - c)
            for r in range(9) for c in range(9)
            if r <= 8 - r and c <= 8 - c
        ]
        random.shuffle(symmetric_pairs)

        for r1, c1, r2, c2 in symmetric_pairs:
            if removed >= cells_to_remove:
                break
            if grid[r1][c1] == 0 or grid[r2][c2] == 0:
                continue

            backup1, backup2 = grid[r1][c1], grid[r2][c2]
            grid[r1][c1], grid[r2][c2] = 0, 0

            if self.has_unique_solution(grid):
                removed += 1 if (r1, c1) == (r2, c2) else 2
            else:
                grid[r1][c1], grid[r2][c2] = backup1, backup2

        return grid
