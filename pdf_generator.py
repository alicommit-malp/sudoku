from fpdf import FPDF

class PDFGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)

    def add_title_page(self, difficulty):
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.cell(0, 100, f'{difficulty.capitalize()} Sudoku Puzzles', ln=True, align='C')

    def add_sudoku_to_pdf(self, sudoku, puzzle_num, difficulty, offset_y, title_suffix="Sudoku Puzzle"):
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.set_xy(0, offset_y - 15)
        self.pdf.cell(210, 10, f'{difficulty.capitalize()} {title_suffix} #{puzzle_num}', ln=True, align='C')

        # Center the puzzle grid horizontally
        cell_size = 10
        offset_x = (210 - 9 * cell_size) / 2  # A4 page width is 210mm

        for i in range(9):
            for j in range(9):
                self.pdf.set_xy(offset_x + j * cell_size, offset_y + i * cell_size)
                value = str(sudoku[i, j]) if sudoku[i, j] != 0 else ""
                self.pdf.set_line_width(0.3)
                self.pdf.cell(cell_size, cell_size, value, border=1, align='C')

        self.pdf.set_line_width(1.5)
        for i in range(0, 10, 3):
            self.pdf.line(offset_x + i * cell_size, offset_y, offset_x + i * cell_size, offset_y + 9 * cell_size)
            self.pdf.line(offset_x, offset_y + i * cell_size, offset_x + 9 * cell_size, offset_y + i * cell_size)

    def generate_puzzles_pdf(self, puzzles, difficulty, is_answer=False):
        self.add_title_page(difficulty if not is_answer else difficulty + " Answers")
        total_puzzles = len(puzzles)
        for i in range(0, total_puzzles, 2):
            self.pdf.add_page()
            # First puzzle
            # If generating answers, use the solutions (puzzles[i][1]), otherwise use the puzzles (puzzles[i][0])
            self.add_sudoku_to_pdf(puzzles[i][1] if is_answer else puzzles[i][0], i + 1, difficulty, offset_y=40, title_suffix="Solution" if is_answer else "Sudoku Puzzle")
            
            # Second puzzle if it exists
            if i + 1 < total_puzzles:
                self.add_sudoku_to_pdf(puzzles[i + 1][1] if is_answer else puzzles[i + 1][0], i + 2, difficulty, offset_y=180, title_suffix="Solution" if is_answer else "Sudoku Puzzle")

    def save_pdf(self, output_file):
        self.pdf.output(output_file)
        print(f"PDF saved as: {output_file}")
