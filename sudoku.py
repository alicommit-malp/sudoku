#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sudoku Puzzle Generator
Author: Ali Alp
Date: September 2024
Description: Generates Sudoku puzzles of varying difficulty (easy, medium, hard), 
and optionally generates an answers PDF with the solution for each puzzle.
"""

import argparse
import sys
from puzzle_generator import PuzzleGenerator
from pdf_generator import PDFGenerator

# --- Main Function ---
def main():
    args = parse_arguments()

    puzzle_generator = PuzzleGenerator()
    pdf_generator = PDFGenerator()

    # Parse config for puzzles
    puzzle_config = {'easy': 0, 'medium': 0, 'hard': 0}
    for config in args.config:
        difficulty, count = config.split(':')
        puzzle_config[difficulty] = int(count)

    # Generate puzzles
    puzzles_generated = {'easy': [], 'medium': [], 'hard': []}
    for difficulty in ['easy', 'medium', 'hard']:
        for _ in range(puzzle_config[difficulty]):
            puzzle, solution = puzzle_generator.generate_sudoku(level=difficulty)
            puzzles_generated[difficulty].append((puzzle, solution))

    # Generate and save puzzle PDFs
    for difficulty in ['easy', 'medium', 'hard']:
        if puzzle_config[difficulty] > 0:
            pdf_generator.generate_puzzles_pdf(puzzles_generated[difficulty], difficulty)

    pdf_generator.save_pdf(args.output)

    # Generate answers PDF if requested
    if args.gen_answers:
        answers_pdf_generator = PDFGenerator()
        for difficulty in ['easy', 'medium', 'hard']:
            if puzzle_config[difficulty] > 0:
                # When generating answers, we pass the solutions instead of puzzles
                answers_pdf_generator.generate_puzzles_pdf(puzzles_generated[difficulty], difficulty, is_answer=True)
        answers_pdf_generator.save_pdf(args.output.replace('.pdf', '_answers.pdf'))


# --- Argument Parser ---
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate Sudoku puzzles PDF",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python main.py -config easy:20 -config medium:30 -output sudoku_puzzles.pdf
  python main.py -config easy:10 -config medium:10 -config hard:10 -output sudoku_puzzles.pdf -gen-answers true
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


if __name__ == "__main__":
    main()
