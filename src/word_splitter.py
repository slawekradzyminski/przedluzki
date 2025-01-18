from pathlib import Path
from typing import List


POLISH_ALPHABET_ORDER = {
    'A': 1, 'Ą': 2, 'B': 3, 'C': 4, 'Ć': 5, 'D': 6, 'E': 7, 'Ę': 8, 'F': 9, 'G': 10,
    'H': 11, 'I': 12, 'J': 13, 'K': 14, 'L': 15, 'Ł': 16, 'M': 17, 'N': 18, 'Ń': 19,
    'O': 20, 'Ó': 21, 'P': 22, 'R': 23, 'S': 24, 'Ś': 25, 'T': 26, 'U': 27, 'W': 28,
    'Y': 29, 'Z': 30, 'Ź': 31, 'Ż': 32
}


def polish_sort_key(word: str) -> List[int]:
    """Create a sort key for a word based on Polish alphabet order."""
    return [POLISH_ALPHABET_ORDER.get(c, 0) for c in word.upper()]


def split_words_by_length(input_file: Path, output_dir: Path):
    """Split words from input file into separate files by length, maintaining Polish order."""
    # Read all words and group by length
    words_by_length = {}
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            if word:
                length = len(word)
                if length not in words_by_length:
                    words_by_length[length] = []
                words_by_length[length].append(word)
    
    # Sort each group by Polish alphabet order and write to files
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for length, words in words_by_length.items():
        output_file = output_dir / f"{length}_letter_words.txt"
        words.sort(key=polish_sort_key)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for word in words:
                f.write(f"{word}\n")
        
        print(f"Created {output_file} with {len(words)} words")


def main():
    # Process both dictionaries
    for dict_name, file_name in [("sjp", "sjp.txt"), ("osps", "osps.txt")]:
        print(f"\nProcessing {dict_name.upper()} dictionary...")
        input_file = Path(f"slowniki/{dict_name}/{file_name}")
        output_dir = Path(f"slowniki/{dict_name}")
        split_words_by_length(input_file, output_dir)


if __name__ == "__main__":
    main()