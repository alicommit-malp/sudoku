import argparse
import sys

class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Generate Sudoku puzzles PDF with optional minimum clues for each difficulty.",
            formatter_class=argparse.RawTextHelpFormatter,
            epilog="""
Examples:
  python sudoku.py -config easy:20:40 -config medium:30:35 --use-symmetry
  python sudoku.py -config hard:10:17 -output sudoku_puzzles.pdf --gen-answers
        """
        )
        self._add_arguments()

    def _add_arguments(self):
        # Puzzle difficulty and number of puzzles in format "easy:20:40" (difficulty:count:clues)
        self.parser.add_argument(
            '-config', 
            action='append', 
            help='Puzzle difficulty and number in format "easy:20", "medium:35", "hard:10".\n'
                 'You can specify multiple difficulties with different counts.',
            required=True
        )

        # Output PDF file name
        self.parser.add_argument(
            '-output', 
            help="Name of the output PDF file (e.g., sudoku_puzzles.pdf).", 
            required=True
        )

        # Generate answers
        self.parser.add_argument(
            '--gen-answers', 
            help="Generate answers in a separate PDF.",
            action='store_true'
        )

        # Use symmetry in puzzle generation
        self.parser.add_argument(
            '--use-symmetry', 
            help="Enable symmetry in puzzle generation (for professional-grade puzzles).", 
            action='store_true'
        )

        # Check if no arguments are provided
        if len(sys.argv) == 1:
            self.parser.print_help(sys.stderr)
            sys.exit(1)

    # Parse the command line arguments
    def parse(self):
        return self.parser.parse_args()
