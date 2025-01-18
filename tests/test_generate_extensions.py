import pytest
from pathlib import Path
from src.generate_extensions import generate_extensions_file, build_extensions_lookup, process_word_batch


def test_build_extensions_lookup():
    """Test building lookup dictionaries for extensions."""
    # given
    extended_words = ["KOTA", "KOTY", "SKOT", "KRET"]
    base_length = 3
    
    # when
    left_lookup, right_lookup = build_extensions_lookup(extended_words, base_length)
    
    # then
    # For each 4-letter word, we get two possible 3-letter words by removing first or last letter
    assert left_lookup == {
        "OTA": ["K"],  # From KOTA
        "OTY": ["K"],  # From KOTY
        "KOT": ["S"],  # From SKOT
        "RET": ["K"]   # From KRET
    }
    assert right_lookup == {
        "KOT": ["A", "Y"],  # From KOTA and KOTY
        "KRE": ["T"],       # From KRET
        "SKO": ["T"]        # From SKOT
    }


def test_process_word_batch():
    """Test processing a batch of words with extension lookups."""
    # given
    words = ["KOT", "PIES"]
    left_lookup = {"KOT": ["S"]}
    right_lookup = {"KOT": ["A", "Y"]}
    
    # when
    result = process_word_batch((words, left_lookup, right_lookup))
    
    # then
    assert len(result) == 2
    assert result[0] == "S KOT A,Y\n"
    assert result[1] == " PIES \n"


def test_generate_extensions_file_normal(tmp_path):
    """Test generating extensions file for normal word length (2-14)."""
    # given
    words_file = tmp_path / "3_letter_words.txt"
    extended_words_file = tmp_path / "4_letter_words.txt"
    extensions_file = tmp_path / "extensions" / "3_letter_extensions.txt"
    
    # Create test files
    with open(words_file, "w", encoding="utf-8") as f:
        f.write("KOT\nPIES\n")
    with open(extended_words_file, "w", encoding="utf-8") as f:
        f.write("KOTA\nKOTY\nSKOT\n")
    
    # when
    generate_extensions_file(words_file, extended_words_file, extensions_file, 3)
    
    # then
    with open(extensions_file, "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f]
    
    assert len(lines) == 2
    assert lines[0] == "S KOT A,Y"
    assert lines[1] == " PIES "


def test_generate_extensions_file_fifteen_letters(tmp_path):
    """Test generating extensions file for 15-letter words (should have no extensions)."""
    # given
    words_file = tmp_path / "15_letter_words.txt"
    extensions_file = tmp_path / "extensions" / "15_letter_extensions.txt"
    
    # Create test file
    with open(words_file, "w", encoding="utf-8") as f:
        f.write("KONSTANTYNOPOL\nPIĘTNASTOLITER\n")
    
    # when
    generate_extensions_file(words_file, None, extensions_file, 15)
    
    # then
    with open(extensions_file, "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f]
    
    assert len(lines) == 2
    assert lines[0] == " KONSTANTYNOPOL "
    assert lines[1] == " PIĘTNASTOLITER " 