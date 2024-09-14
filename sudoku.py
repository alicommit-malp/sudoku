#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sudoku Puzzle Generator
Author: [Ali Alp]
Date: [September 2024]
Description: Generates Sudoku puzzles of varying difficulty (easy, medium, hard), 
and optionally generates an answers PDF with the solution for each puzzle.
"""

import argparse
import sys
import numpy as np
from fpdf import FPDF

# Improved argument parser
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate Sudoku puzzles PDF",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python sudoku.py -config easy:20 -config medium:30 -output sudoku_puzzles.pdf
  python sudoku.py -config easy:10 -config medium:10 -config hard:10 -output sudoku_puzzles.pdf -gen-answers true
        """
    )

    parser.add_argument(
        '-config', 
        action='append', 
        help='Puzzle difficulty and number in format "easy:20", "medium:35", "hard:10".\n'
             'You can specify multiple difficulties with different counts.',
        required=True
    )

    parser.add_argument(
        '-output', 
        help="Name of the output PDF file (e.g., sudoku_puzzles.pdf).", 
        required=True
    )

    parser.add_argument(
        '-gen-answers', 
        help="Generate answers in a separate PDF. Set to 'true' to enable.", 
        type=bool, 
        default=False
    )

    # Check if no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Parse the arguments
    return parser.parse_args()

# Function to add a title page for each difficulty
def add_title_page(pdf, difficulty):
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 100, f'{difficulty.capitalize()} Sudoku Puzzles', ln=True, align='C')

# Sudoku generation helper functions
def is_valid(board, row, col, num):
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

def fill_grid(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                num_list = list(range(1, 10))
                np.random.shuffle(num_list)
                for num in num_list:
                    if is_valid(grid, i, j, num):
                        grid[i][j] = num
                        if fill_grid(grid):
                            return True
                        grid[i][j] = 0
                return False
    return True

def generate_sudoku(level="medium"):
    grid = np.zeros((9, 9), dtype=int)
    fill_grid(grid)
    puzzle = remove_numbers(grid.copy(), level)
    return puzzle, grid  # Return both the puzzle and the solution

def remove_numbers(grid, level="medium"):
    if level == "easy":
        attempts = 35
    elif level == "medium":
        attempts = 45
    else:  # hard
        attempts = 55
    while attempts > 0:
        row = np.random.randint(9)
        col = np.random.randint(9)
        while grid[row][col] == 0:
            row = np.random.randint(9)
            col = np.random.randint(9)
        grid[row][col] = 0
        attempts -= 1
    return grid

# Function to add a Sudoku puzzle (and answer if requested) to the PDF
def add_sudoku_to_pdf(pdf, sudoku, puzzle_num, difficulty, offset_y, title_suffix="Sudoku Puzzle"):
    pdf.set_font('Arial', 'B', 16)
    # Center the title horizontally
    pdf.set_xy(0, offset_y - 15)  # Add 15px margin above the puzzle for the title
    pdf.cell(210, 10, f'{difficulty.capitalize()} {title_suffix} #{puzzle_num}', ln=True, align='C')

    # Center horizontally for the puzzle grid
    cell_size = 10
    offset_x = (210 - 9 * cell_size) / 2  # Centered horizontally on A4 paper

    # Draw the Sudoku puzzle grid
    for i in range(9):
        for j in range(9):
            pdf.set_xy(offset_x + j * cell_size, offset_y + i * cell_size)
            value = str(sudoku[i, j]) if sudoku[i, j] != 0 else ""
            pdf.set_line_width(0.3)  # Regular border for cells
            pdf.cell(cell_size, cell_size, value, border=1, align='C')

    # Draw thicker borders for the 3x3 subgrids
    pdf.set_line_width(1.5)
    for i in range(0, 10, 3):
        pdf.line(offset_x + i * cell_size, offset_y, offset_x + i * cell_size, offset_y + 9 * cell_size)
        pdf.line(offset_x, offset_y + i * cell_size, offset_x + 9 * cell_size, offset_y + i * cell_size)

# Function to handle puzzle addition based on count with proper spacing
def add_puzzles_with_title(pdf, puzzles, difficulty, title=True, is_answer=False):
    if title:
        add_title_page(pdf, difficulty if not is_answer else difficulty + " Answers")
    
    total_puzzles = len(puzzles)
    for i in range(0, total_puzzles, 2):
        pdf.add_page()
        # Add the first puzzle on this page at offset_y=40
        if not is_answer:
            add_sudoku_to_pdf(pdf, puzzles[i][0], i + 1, difficulty, offset_y=40)
        else:
            add_sudoku_to_pdf(pdf, puzzles[i][1], i + 1, difficulty, offset_y=40, title_suffix="Solution")

        # If there's an even number of puzzles, add the second one on the same page at offset_y=160
        if i + 1 < total_puzzles:
            if not is_answer:
                add_sudoku_to_pdf(pdf, puzzles[i + 1][0], i + 2, difficulty, offset_y=180)
            else:
                add_sudoku_to_pdf(pdf, puzzles[i + 1][1], i + 2, difficulty, offset_y=180, title_suffix="Solution")

def main():
    # Parse arguments
    args = parse_arguments()

    # Dictionary to store number of puzzles per difficulty
    puzzle_config = {'easy': 0, 'medium': 0, 'hard': 0}

    # Parse the config arguments (e.g. 'easy:25')
    for config in args.config:
        difficulty, count = config.split(':')
        puzzle_config[difficulty] = int(count)

    # Create a new PDF for the puzzles
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Create another PDF for the answers if required
    if args.gen_answers:
        answers_pdf = FPDF()
        answers_pdf.set_auto_page_break(auto=True, margin=15)

    # Generate puzzles and answers, and add them to the PDF
    puzzles_generated = {'easy': [], 'medium': [], 'hard': []}
    for difficulty in ['easy', 'medium', 'hard']:
        for _ in range(puzzle_config[difficulty]):
            puzzle, answer = generate_sudoku(level=difficulty)
            puzzles_generated[difficulty].append((puzzle, answer))

    # Add puzzles in the order of easy, medium, hard
    for difficulty in ['easy', 'medium', 'hard']:
        if puzzle_config[difficulty] > 0:
            add_puzzles_with_title(pdf, puzzles_generated[difficulty], difficulty)

            if args.gen_answers:
                add_puzzles_with_title(answers_pdf, puzzles_generated[difficulty], difficulty, title=True, is_answer=True)

    # Save the final puzzle PDF
    pdf_output_path = args.output
    pdf.output(pdf_output_path)
    print(f"Sudoku PDF generated: {pdf_output_path}")

    # Save the answers PDF if required
    if args.gen_answers:
        answers_output_path = pdf_output_path.replace('.pdf', '_answers.pdf')
        answers_pdf.output(answers_output_path)
        print(f"Answers PDF generated: {answers_output_path}")

if __name__ == "__main__":
    main()
