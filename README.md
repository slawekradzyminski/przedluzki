# Przedłużki

A tool for generating word extensions in Polish language.

## Obtaining files

### OSPS

- Download latest update from http://www.pfs.org.pl/osps_aktualizacje.php
- Create `words.txt` using https://github.com/slawekradzyminski/psps

### SJP

- Download from https://sjp.pl/sl/growy/

## Process

The tool works in three steps:

1. Word Splitting (`word_splitter.py`)
   - Reads words from input dictionaries (`sjp.txt` and `osps.txt`)
   - Groups words by length (2-15 letters)
   - Sorts each group according to Polish alphabetical order
   - Creates separate files for each word length (e.g., `2_letter_words.txt`, `3_letter_words.txt`, etc.)

2. Extensions Generation (`generate_extensions.py`)
   - For each word length (2-14):
     - Takes words from `n_letter_words.txt`
     - Finds possible extensions using `(n+1)_letter_words.txt`
     - Creates `n_letter_extensions.txt` with format: "LEFT_EXTENSIONS WORD RIGHT_EXTENSIONS"
   - For 15-letter words:
     - Creates `15_letter_extensions.txt` with empty extensions

3. PDF Generation (`generate_pdfs.py`)
   - Creates PDFs from the extension files
   - Each PDF contains three columns:
     - Left extensions (without commas)
     - Original word (in uppercase)
     - Right extensions (without commas)
   - Uses Arial Unicode MS font for proper Polish character support
   - Optimized for performance with batch processing
   - Maintains consistent formatting with grey headers and grid lines

### Performance Optimizations

The extension generation is optimized for performance using:
1. Dictionary lookups instead of linear searches
2. Parallel processing with multiprocessing
3. Batch processing of words (1000 words per batch)
4. Pre-computed extension lookups
5. Efficient string handling

The PDF generation is optimized using:
1. Batch processing of rows (1000 per batch)
2. Single font registration
3. Reusable table styles
4. Memory-efficient data handling
5. Proportional column widths

This allows processing large files (400k+ words) quickly and efficiently.

### Polish Alphabet Order

The script follows the official Polish alphabet order:
```
A, Ą, B, C, Ć, D, E, Ę, F, G, H, I, J, K, L, Ł, M, N, Ń, O, Ó, P, R, S, Ś, T, U, W, Y, Z, Ź, Ż
```

### Output Format

Extensions files follow this format:
- Each line: `LEFT_EXTENSIONS WORD RIGHT_EXTENSIONS`
- Extensions are comma-separated letters
- Words without extensions have spaces on both sides
- Example: `B,C,D KOT A,Y`

### Usage

1. Split words by length:
```bash
python src/word_splitter.py
```

2. Generate extensions:
```bash
python src/generate_extensions.py
```

3. Generate PDFs:
```bash
python src/generate_pdfs.py
```

### Testing

Run all tests with:
```bash
pytest tests/test_word_splitter.py tests/test_generate_extensions.py tests/test_generate_pdfs.py -v
```

The tests verify:
- Correct Polish alphabetical ordering
- Proper handling of all Polish diacritical marks
- Correct file splitting by word length
- Proper extension generation for all word lengths
- Special handling of 15-letter words
- Parallel processing and batch handling
- Extension lookup optimization
- PDF generation and formatting
- Word order preservation
- Extension parsing accuracy