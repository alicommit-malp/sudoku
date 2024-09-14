#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sudoku Puzzle Generator with multiprocessing support to use all cores
Author: [Ali Alp]
Date: September 2024
Description: Generates Sudoku puzzles of varying difficulty (easy, medium, hard),
with optional minimum clues for each difficulty level, and optionally generates an answers PDF with the solution.
Supports parallel processing to utilize all CPU cores for generating puzzles concurrently.
"""

from multiprocessing import Pool, cpu_count
from advanced_sudoku_generator import AdvancedSudokuGenerator
from pdf_generator import PDFGenerator
from argument_parser import ArgumentParser

# Helper function for multiprocessing
def generate_puzzle_task(task):
    min_clues, difficulty, use_symmetry = task
    generator = AdvancedSudokuGenerator()
    return generator.generate_professional_sudoku(min_clues=min_clues, symmetry=use_symmetry, required_difficulty=difficulty)

# Main Function
def main():
    # Use the ArgumentParser class to parse arguments
    args_parser = ArgumentParser()
    args = args_parser.parse()

    pdf_generator = PDFGenerator()

    # Parse puzzle configurations
    puzzle_config = {'easy': [], 'medium': [], 'hard': []}

    # Handle the config to extract difficulty, count, and optional min_clues
    for config in args.config:
        parts = config.split(':')
        difficulty = parts[0]
        count = int(parts[1])
        min_clues = int(parts[2]) if len(parts) == 3 else get_default_min_clues(difficulty)

        # Validate that min_clues is at least 17
        if min_clues < 17:
            raise ValueError(f"Error: Minimum clues must be at least 17. You provided {min_clues} for {difficulty}.")

        puzzle_config[difficulty].append({'count': count, 'min_clues': min_clues})

    # Prepare tasks for multiprocessing
    tasks = []
    for difficulty in ['easy', 'medium', 'hard']:
        for config in puzzle_config[difficulty]:
            for _ in range(config['count']):
                tasks.append((config['min_clues'], difficulty, args.use_symmetry))

    # Use multiprocessing to generate puzzles in parallel
    num_cores = cpu_count()  # Get the number of CPU cores available
    print(f"Generating puzzles using {num_cores} CPU cores...")

    # Check multiprocessing setup
    print(f"Number of tasks to process: {len(tasks)}")
    with Pool(processes=num_cores) as pool:
        puzzles_generated_flat = pool.map(generate_puzzle_task, tasks)

    # Restructure the puzzles back into their difficulty groups
    puzzles_generated = {'easy': [], 'medium': [], 'hard': []}
    index = 0
    for difficulty in ['easy', 'medium', 'hard']:
        for config in puzzle_config[difficulty]:
            puzzles_generated[difficulty].extend(puzzles_generated_flat[index:index + config['count']])
            index += config['count']

    # Generate and save puzzle PDFs
    for difficulty in ['easy', 'medium', 'hard']:
        if len(puzzles_generated[difficulty]) > 0:
            pdf_generator.generate_puzzles_pdf(puzzles_generated[difficulty], difficulty)

    pdf_generator.save_pdf(args.output)

    # Generate answers PDF if requested
    if args.gen_answers:
        answers_pdf_generator = PDFGenerator()
        for difficulty in ['easy', 'medium', 'hard']:
            if len(puzzles_generated[difficulty]) > 0:
                answers_pdf_generator.generate_puzzles_pdf(puzzles_generated[difficulty], difficulty, is_answer=True)
        answers_pdf_generator.save_pdf(args.output.replace('.pdf', '_answers.pdf'))

# --- Default Min Clues Based on Difficulty ---
def get_default_min_clues(difficulty):
    """
    Get the default minimum clues for a given difficulty.
    """
    if difficulty == 'easy':
        return 40
    elif difficulty == 'medium':
        return 35
    elif difficulty == 'hard':
        return 30
    else:
        raise ValueError(f"Unknown difficulty level: {difficulty}")


if __name__ == "__main__":
    main()  # Ensure main() is executed directly to avoid multiprocessing issues
