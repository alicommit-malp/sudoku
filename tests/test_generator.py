"""Tests for the Sudoku generator.

Run from the repo root:
    python -m unittest discover tests

Most tests pin random.seed for reproducibility, but the invariants under
test (uniqueness, symmetry, consistency) hold for any seed.
"""

import os
import random
import sys
import unittest
from unittest import mock

import numpy as np

# Make the project root importable when running the test file directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from advanced_sudoku_generator import AdvancedSudokuGenerator
from argument_parser import ArgumentParser
from puzzle_generator import PuzzleGenerator


# ----- Helpers -----

def is_valid_sudoku_state(grid):
    """Every nonzero cell respects row / col / box rules."""
    for i in range(9):
        row = [v for v in grid[i] if v != 0]
        col = [grid[r][i] for r in range(9) if grid[r][i] != 0]
        if len(row) != len(set(row)) or len(col) != len(set(col)):
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            box = [grid[br + i][bc + j]
                   for i in range(3) for j in range(3)
                   if grid[br + i][bc + j] != 0]
            if len(box) != len(set(box)):
                return False
    return True


def is_complete(grid):
    return all(grid[r][c] != 0 for r in range(9) for c in range(9))


def is_180_symmetric(grid):
    """Pattern of givens is 180° rotationally symmetric."""
    return all((grid[r][c] != 0) == (grid[8 - r][8 - c] != 0)
               for r in range(9) for c in range(9))


# ----- PuzzleGenerator -----

class TestPuzzleGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PuzzleGenerator()

    def test_is_valid_empty_grid(self):
        g = np.zeros((9, 9), dtype=int)
        for n in range(1, 10):
            self.assertTrue(self.gen.is_valid(g, 0, 0, n))

    def test_is_valid_row_conflict(self):
        g = np.zeros((9, 9), dtype=int)
        g[3][0] = 7
        self.assertFalse(self.gen.is_valid(g, 3, 5, 7))
        self.assertTrue(self.gen.is_valid(g, 3, 5, 8))

    def test_is_valid_col_conflict(self):
        g = np.zeros((9, 9), dtype=int)
        g[0][4] = 5
        self.assertFalse(self.gen.is_valid(g, 7, 4, 5))
        self.assertTrue(self.gen.is_valid(g, 7, 4, 6))

    def test_is_valid_box_conflict(self):
        g = np.zeros((9, 9), dtype=int)
        g[0][0] = 9
        self.assertFalse(self.gen.is_valid(g, 2, 2, 9))  # same 3x3 box
        self.assertTrue(self.gen.is_valid(g, 3, 3, 9))   # different box

    def test_fill_grid_produces_valid_complete_sudoku(self):
        g = np.zeros((9, 9), dtype=int)
        self.assertTrue(self.gen.fill_grid(g))
        self.assertTrue(is_complete(g))
        self.assertTrue(is_valid_sudoku_state(g))

    def test_count_solutions_respects_cap(self):
        # An empty grid has billions of solutions; the cap should stop early.
        empty = np.zeros((9, 9), dtype=int)
        self.assertEqual(self.gen.count_solutions(empty, cap=2), 2)
        self.assertEqual(self.gen.count_solutions(empty, cap=1), 1)

    def test_count_solutions_on_complete_grid(self):
        g = np.zeros((9, 9), dtype=int)
        self.gen.fill_grid(g)
        self.assertEqual(self.gen.count_solutions(g), 1)

    def test_has_unique_solution_complete(self):
        g = np.zeros((9, 9), dtype=int)
        self.gen.fill_grid(g)
        self.assertTrue(self.gen.has_unique_solution(g))

    def test_has_unique_solution_empty(self):
        g = np.zeros((9, 9), dtype=int)
        self.assertFalse(self.gen.has_unique_solution(g))

    def test_remove_numbers_exact_clues_preserves_uniqueness(self):
        g = np.zeros((9, 9), dtype=int)
        self.gen.fill_grid(g)
        puzzle = self.gen.remove_numbers_exact_clues(g.copy(), num_clues=40)
        self.assertTrue(self.gen.has_unique_solution(puzzle))
        # Achieved clues must be at least the requested target — we never
        # remove more than `81 - num_clues` cells.
        self.assertGreaterEqual(int(np.count_nonzero(puzzle)), 40)


# ----- AdvancedSudokuGenerator -----

class TestAdvancedSudokuGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(123)
        self.gen = AdvancedSudokuGenerator()

    def assertWellFormed(self, puzzle, solution):
        self.assertTrue(is_complete(solution), "solution must be fully filled")
        self.assertTrue(is_valid_sudoku_state(solution), "solution must satisfy sudoku rules")
        self.assertTrue(self.gen.has_unique_solution(puzzle), "puzzle must have a unique solution")
        for r in range(9):
            for c in range(9):
                if puzzle[r][c] != 0:
                    self.assertEqual(
                        puzzle[r][c], solution[r][c],
                        f"given at ({r},{c}) does not match the unique solution",
                    )

    def test_easy_puzzle_well_formed(self):
        puzzle, sol = self.gen.generate_professional_sudoku(min_clues=40, symmetry=False)
        self.assertWellFormed(puzzle, sol)

    def test_medium_puzzle_well_formed(self):
        puzzle, sol = self.gen.generate_professional_sudoku(min_clues=35, symmetry=False)
        self.assertWellFormed(puzzle, sol)

    def test_hard_puzzle_well_formed(self):
        puzzle, sol = self.gen.generate_professional_sudoku(min_clues=30, symmetry=False)
        self.assertWellFormed(puzzle, sol)

    def test_min_clues_is_lower_bound(self):
        for target in (30, 35, 40):
            puzzle, _ = self.gen.generate_professional_sudoku(min_clues=target, symmetry=False)
            self.assertGreaterEqual(
                int(np.count_nonzero(puzzle)), target,
                f"target {target}: achieved clue count must be >= target",
            )

    def test_symmetric_puzzle_is_180_symmetric(self):
        # Regression: the old `enforce_exact_clue_count` post-pass forcibly
        # removed cells without preserving symmetry.
        for _ in range(3):
            puzzle, sol = self.gen.generate_professional_sudoku(min_clues=30, symmetry=True)
            self.assertTrue(is_180_symmetric(puzzle), "symmetric mode produced asymmetric givens")
            self.assertWellFormed(puzzle, sol)

    def test_symmetric_aggressive_target_remains_unique(self):
        # Regression for the headline bug: hard + symmetry + 25 clues used to
        # produce non-unique puzzles (the brute-force enforce pass ripped out
        # cells without checking uniqueness).
        for _ in range(3):
            puzzle, sol = self.gen.generate_professional_sudoku(min_clues=25, symmetry=True)
            self.assertTrue(self.gen.has_unique_solution(puzzle))
            self.assertTrue(is_180_symmetric(puzzle))
            self.assertWellFormed(puzzle, sol)

    def test_center_cell_counts_as_one_when_symmetric(self):
        # Regression: in the symmetric removal loop the center cell (4,4) is
        # its own pair, so removing it must increment the counter by 1 — not 2.
        # We can't observe the counter directly, but we can verify the broader
        # invariant: with --use-symmetry the achieved clue count is never less
        # than the lower-bounded target.
        for target in (30, 35, 40):
            puzzle, _ = self.gen.generate_professional_sudoku(min_clues=target, symmetry=True)
            self.assertGreaterEqual(int(np.count_nonzero(puzzle)), target)


# ----- ArgumentParser -----

class TestArgumentParser(unittest.TestCase):
    def test_construction_has_no_side_effects(self):
        # Regression: previously the no-args check lived in __init__ and
        # called sys.exit(1) — making the class unusable from tests / REPL.
        with mock.patch.object(sys, 'argv', ['sudoku.py']):
            ArgumentParser()  # must not raise / exit

    def test_parse_basic(self):
        argv = ['sudoku.py', '-config', 'easy:5:40', '-output', 'out.pdf']
        with mock.patch.object(sys, 'argv', argv):
            args = ArgumentParser().parse()
        self.assertEqual(args.config, ['easy:5:40'])
        self.assertEqual(args.output, 'out.pdf')
        self.assertFalse(args.use_symmetry)
        self.assertFalse(args.gen_answers)

    def test_parse_with_flags(self):
        argv = ['sudoku.py', '-config', 'hard:1:30', '-output', 'out.pdf',
                '--use-symmetry', '--gen-answers']
        with mock.patch.object(sys, 'argv', argv):
            args = ArgumentParser().parse()
        self.assertTrue(args.use_symmetry)
        self.assertTrue(args.gen_answers)

    def test_parse_multiple_configs(self):
        argv = ['sudoku.py',
                '-config', 'easy:10:40',
                '-config', 'medium:5:35',
                '-output', 'out.pdf']
        with mock.patch.object(sys, 'argv', argv):
            args = ArgumentParser().parse()
        self.assertEqual(args.config, ['easy:10:40', 'medium:5:35'])


if __name__ == '__main__':
    unittest.main()
