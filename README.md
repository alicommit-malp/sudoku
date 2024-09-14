# Free Sudoku Puzzel Generator

![Sample Puzzle](./samples/sample_puzzle.png)

[Sample Puzzle PDF](./samples/sudoku_puzzles.pdf)

[Sample Puzzle Answers PDF](./samples/sudoku_puzzles_answers.pdf)

## Description

This project is a command-line Sudoku Puzzle Generator written in Python. It allows you to generate Sudoku puzzles of varying difficulty (easy, medium, and hard) and optionally generate an answer key in a separate PDF.

The script generates Sudoku puzzles in PDF format and can also generate a second PDF containing the answers (solutions) for each puzzle.

---

## Features

- Generate Sudoku puzzles of different difficulty levels: `easy`, `medium`, `hard`.
- Output the puzzles in a PDF.
- Optionally generate answers (solutions) in a separate PDF.
- Supports multiple difficulty levels and puzzle counts in one run.

---

## Requirements

- Python 3.x
- [FPDF](https://pyfpdf.github.io/) Python library for PDF generation.
  
To install the required packages, run:

```bash
pip install fpdf numpy
```

---

## How to Use

Make sure the script is executable. You can do this by running:

```bash
chmod +x sudoku_gen.py
```

### Basic Usage

You can generate Sudoku puzzles by specifying the difficulty and number of puzzles per difficulty.

```bash
./sudoku_gen.py -config easy:10 -output sudoku_puzzles.pdf
```

The command above generates 10 easy puzzles and saves them in a PDF file named `sudoku_puzzles.pdf`.

---

### Parameters

- **`-config`**: Specifies the difficulty and number of puzzles. Format: `"difficulty:number"`. You can use multiple `-config` parameters for different difficulties.
  - Example: `-config easy:10 -config medium:15 -config hard:5`
- **`-output`**: The name of the output PDF file for the puzzles.
  - Example: `-output sudoku_puzzles.pdf`
- **`-gen-answers`**: Optionally generate a second PDF with the answers (solutions) to the puzzles. Set this to `true` to enable this feature.
  - Example: `-gen-answers true`

---

### Examples

1. **Generate 10 easy Sudoku puzzles and save them to a PDF**:

```bash
./sudoku_gen.py -config easy:10 -output sudoku_puzzles.pdf
```

2. **Generate 10 easy puzzles, 15 medium puzzles, and 5 hard puzzles, all in the same PDF**:

```bash
./sudoku_gen.py -config easy:10 -config medium:15 -config hard:5 -output sudoku_puzzles.pdf
```

3. **Generate 5 easy puzzles, 5 medium puzzles, and 5 hard puzzles, and generate a second PDF with the answers**:

```bash
./sudoku_gen.py -config easy:5 -config medium:5 -config hard:5 -output sudoku_puzzles.pdf -gen-answers true
```

---

## Output

- **Puzzle PDF**: The script will generate a PDF containing the Sudoku puzzles. Each difficulty level starts with a title page.
- **Answers PDF (optional)**: If you enable the `-gen-answers` flag, the script generates a second PDF with the solutions to the puzzles in the same order.

---

## License

MIT License. Feel free to use and modify this project for personal or commercial use.

