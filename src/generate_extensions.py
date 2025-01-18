from pathlib import Path
from multiprocessing import Pool, cpu_count
from typing import List, Tuple, Dict


def read_words(file_path: Path) -> List[str]:
    """Read words from a file, maintaining original order."""
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip().upper() for line in f if line.strip()]


def build_extensions_lookup(extended_words: List[str], base_length: int) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """Build lookup dictionaries for left and right extensions."""
    left_extensions = {}
    right_extensions = {}
    
    for extended_word in extended_words:
        # Left extensions
        word_without_first = extended_word[1:]
        if len(word_without_first) == base_length:
            if word_without_first not in left_extensions:
                left_extensions[word_without_first] = []
            left_extensions[word_without_first].append(extended_word[0])
        
        # Right extensions
        word_without_last = extended_word[:-1]
        if len(word_without_last) == base_length:
            if word_without_last not in right_extensions:
                right_extensions[word_without_last] = []
            right_extensions[word_without_last].append(extended_word[-1])
    
    return left_extensions, right_extensions


def format_extensions_line(word: str, left_ext: List[str], right_ext: List[str]) -> str:
    """Format a line with extensions, ensuring spaces around the word."""
    left_str = ",".join(left_ext) if left_ext else ""
    right_str = ",".join(right_ext) if right_ext else ""
    return f"{left_str} {word} {right_str}\n"


def process_word_batch(args: Tuple[List[str], Dict[str, List[str]], Dict[str, List[str]]]) -> List[str]:
    """Process a batch of words using extension lookups."""
    words, left_lookup, right_lookup = args
    result = []
    
    for word in words:
        left_ext = left_lookup.get(word, [])
        right_ext = right_lookup.get(word, [])
        result.append(format_extensions_line(word, left_ext, right_ext))
    
    return result


def generate_extensions_file(words_file: Path, extended_words_file: Path, extensions_file: Path, word_length: int):
    """Generate extensions file from words file and extended words file."""
    words = read_words(words_file)
    
    # For 15-letter words, just write them with empty extensions
    if word_length == 15:
        extensions_file.parent.mkdir(parents=True, exist_ok=True)
        with open(extensions_file, "w", encoding="utf-8") as f:
            for word in words:
                f.write(f" {word} \n")
        print(f"Processed {len(words)} words (no extensions for 15-letter words)")
        return
    
    # For other lengths, find extensions from the next length
    extended_words = read_words(extended_words_file)
    
    # Build lookup dictionaries
    left_lookup, right_lookup = build_extensions_lookup(extended_words, len(words[0]))
    
    # Ensure parent directory exists
    extensions_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Process words in parallel
    batch_size = 1000
    batches = [words[i:i + batch_size] for i in range(0, len(words), batch_size)]
    
    with Pool(cpu_count()) as pool:
        results = pool.map(process_word_batch, 
                         [(batch, left_lookup, right_lookup) for batch in batches])
    
    # Write results
    with open(extensions_file, "w", encoding="utf-8") as f:
        for batch_result in results:
            f.writelines(batch_result)
    
    print(f"Processed {len(words)} words")


def main():
    # Process both dictionaries for all word lengths
    for dict_name in ["sjp", "osps"]:
        print(f"\nProcessing {dict_name.upper()} dictionary...")
        
        for length in range(2, 16):
            words_file = Path(f"slowniki/{dict_name}/{length}_letter_words.txt")
            if not words_file.exists():
                print(f"Skipping {length}-letter words (file not found)")
                continue
                
            extensions_file = Path(f"slowniki/{dict_name}/extensions/{length}_letter_extensions.txt")
            
            if length < 15:
                extended_words_file = Path(f"slowniki/{dict_name}/{length + 1}_letter_words.txt")
                if not extended_words_file.exists():
                    print(f"Skipping {length}-letter words (no extended words file)")
                    continue
                    
                print(f"Processing {length}-letter words...")
                print(f"Reading words from {words_file}")
                print(f"Finding extensions using {extended_words_file}")
                generate_extensions_file(words_file, extended_words_file, extensions_file, length)
            else:
                print(f"Processing {length}-letter words (no extensions)...")
                generate_extensions_file(words_file, None, extensions_file, length)
                
            print(f"Created {extensions_file}")


if __name__ == "__main__":
    main()