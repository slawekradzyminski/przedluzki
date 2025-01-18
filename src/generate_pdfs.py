from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from typing import List, Tuple


# Register fonts only once at module level
pdfmetrics.registerFont(TTFont('CustomFont', '/Library/Fonts/Arial Unicode.ttf'))

# Define table style once
TABLE_STYLE = TableStyle([
    # Header row style
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'CustomFont'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    # Data rows
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'CustomFont'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('TOPPADDING', (0, 1), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
])

# Constants
BATCH_SIZE = 1000
HEADER = ['Left Extensions', 'Word', 'Right Extensions']


def parse_extensions_line(line: str, word_length: int) -> Tuple[str, str, str]:
    """Parse a line from extensions file into left extensions, word, and right extensions.
    
    Example lines:
     AAA                        -> no extensions
    B,L,Ł,Ż ABO               -> left extensions only
    B,C,D,L,P,R,T,Ł,Ż ABY M,Ś -> both extensions
    """
    parts = line.strip().split()
    
    # Find the word (of specified length, no commas)
    word_idx = -1
    for i, part in enumerate(parts):
        if len(part) == word_length and ',' not in part:
            word_idx = i
            break
            
    if word_idx == -1:
        return "", "", ""  # No valid word found
        
    # Extract word
    word = parts[word_idx]
    
    # Get left extensions (everything before the word)
    left_ext = " ".join(parts[:word_idx])
    
    # Get right extensions (everything after the word)
    right_ext = " ".join(parts[word_idx + 1:])
    
    return left_ext, word, right_ext


def format_extensions(ext_str: str) -> str:
    """Format extensions string by removing commas."""
    return ext_str.replace(",", "") if ext_str else ""


def process_batch(lines: List[str], word_length: int) -> List[List[str]]:
    """Process a batch of lines into table data."""
    table_data = []
    for line in lines:
        left_ext, word, right_ext = parse_extensions_line(line, word_length)
        if word:  # Only add if we found a valid word
            table_data.append([
                format_extensions(left_ext),
                word,
                format_extensions(right_ext)
            ])
    return table_data


def create_pdf(extensions_file: Path, output_file: Path, word_length: int, dict_name: str):
    """Create PDF from extensions file using batch processing."""
    # Read all lines first
    with open(extensions_file, 'r', encoding='utf-8') as f:
        all_lines = [line.strip() for line in f if line.strip()]
    
    # Create PDF document
    doc = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    
    # Calculate column widths (as percentages of page width)
    col_widths = [
        doc.width * 0.35,  # Left extensions
        doc.width * 0.3,   # Word
        doc.width * 0.35   # Right extensions
    ]
    
    # Process data in batches
    elements = []
    table_data = [HEADER]  # Start with header
    
    for i in range(0, len(all_lines), BATCH_SIZE):
        batch = all_lines[i:i + BATCH_SIZE]
        table_data.extend(process_batch(batch, word_length))
        
        # If batch is full or this is the last batch, create table and reset
        if len(table_data) >= BATCH_SIZE or i + BATCH_SIZE >= len(all_lines):
            if len(table_data) > 1:  # Only create table if we have data beyond header
                table = Table(table_data, colWidths=col_widths)
                table.setStyle(TABLE_STYLE)
                elements.append(table)
            table_data = [HEADER]  # Reset with header for next batch
    
    # Build PDF
    if elements:  # Only build if we have tables to add
        doc.build(elements)
        print(f"Created {output_file} with {sum(len(batch) - 1 for batch in elements)} words")
    else:
        print(f"No valid {word_length}-letter words found in {extensions_file}")


def main():
    # Process both dictionaries
    for dict_name in ["sjp", "osps"]:
        print(f"\nProcessing {dict_name.upper()} dictionary...")
        
        for length in range(2, 16):
            extensions_file = Path(f"slowniki/{dict_name}/extensions/{length}_letter_extensions.txt")
            if not extensions_file.exists():
                print(f"Skipping {dict_name.upper()}{length} (extensions file not found)")
                continue
                
            output_file = Path(f"slowniki/{dict_name}/{dict_name.upper()}{length}.pdf")
            print(f"Processing {dict_name.upper()}{length}...")
            
            create_pdf(extensions_file, output_file, length, dict_name)


if __name__ == "__main__":
    main()