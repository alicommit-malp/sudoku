# puzzle_generator.py
import numpy as np

class PuzzleGenerator:
    def __init__(self):
        pass

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

    def fill_grid(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    num_list = list(range(1, 10))
                    np.random.shuffle(num_list)
                    for num in num_list:
                        if self.is_valid(grid, i, j, num):
                            grid[i][j] = num
                            if self.fill_grid(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True

    def remove_numbers(self, grid, level="medium"):
        attempts = 60 if level == "professional" else (45 if level == "hard" else 35)
        while attempts > 0:
            row, col = np.random.randint(0, 9), np.random.randint(0, 9)
            while grid[row][col] == 0:
                row, col = np.random.randint(0, 9), np.random.randint(0, 9)
            backup = grid[row][col]
            grid[row][col] = 0
            if not self.has_unique_solution(grid.copy()):
                grid[row][col] = backup  # Restore if not unique
            else:
                attempts -= 1
        return grid

    def has_unique_solution(self, grid):
        return self.count_solutions(grid.copy()) == 1

    def count_solutions(self, grid):
        count = [0]
        self.solve(grid.copy(), count)
        return count[0]

    def solve(self, grid, count):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(grid, i, j, num):
                            grid[i][j] = num
                            self.solve(grid, count)
                            grid[i][j] = 0
                    return
        count[0] += 1

    def generate_sudoku(self, level="medium"):
        grid = np.zeros((9, 9), dtype=int)
        self.fill_grid(grid)
        puzzle = self.remove_numbers(grid.copy(), level)
        return puzzle, grid  # Return the puzzle and solution
