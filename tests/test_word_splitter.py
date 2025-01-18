import pytest
from pathlib import Path
from src.word_splitter import polish_sort_key, split_words_by_length


def test_polish_sort_key():
    """Test that polish_sort_key correctly orders words according to Polish alphabet."""
    # given
    words = ["łab", "lab", "łąb", "ząb", "zab", "żab"]
    expected_order = ["lab", "łab", "łąb", "zab", "ząb", "żab"]
    
    # when
    sorted_words = sorted(words, key=polish_sort_key)
    
    # then
    assert sorted_words == expected_order


def test_polish_sort_key_with_diacritics():
    """Test handling of all Polish diacritical marks."""
    # given
    words = ["a", "ą", "c", "ć", "e", "ę", "l", "ł", "n", "ń", "o", "ó", "s", "ś", "z", "ź", "ż"]
    expected_order = ["a", "ą", "c", "ć", "e", "ę", "l", "ł", "n", "ń", "o", "ó", "s", "ś", "z", "ź", "ż"]
    
    # when
    sorted_words = sorted(words, key=polish_sort_key)
    
    # then
    assert sorted_words == expected_order


def test_split_words_by_length(tmp_path):
    """Test splitting words into files by length while maintaining Polish order."""
    # given
    input_file = tmp_path / "test_words.txt"
    output_dir = tmp_path / "output"
    
    test_words = [
        "ab", "ąb", "abc", "ąbc", "abcd",
        "żab", "źab", "łab", "lab"
    ]
    
    with open(input_file, "w", encoding="utf-8") as f:
        for word in test_words:
            f.write(f"{word}\n")
    
    # when
    split_words_by_length(input_file, output_dir)
    
    # then
    # Check 2-letter words
    with open(output_dir / "2_letter_words.txt", "r", encoding="utf-8") as f:
        two_letter_words = [line.strip() for line in f]
    assert two_letter_words == ["ab", "ąb"]
    
    # Check 3-letter words
    with open(output_dir / "3_letter_words.txt", "r", encoding="utf-8") as f:
        three_letter_words = [line.strip() for line in f]
    assert three_letter_words == ["abc", "ąbc", "lab", "łab", "źab", "żab"]
    
    # Check 4-letter words
    with open(output_dir / "4_letter_words.txt", "r", encoding="utf-8") as f:
        four_letter_words = [line.strip() for line in f]
    assert four_letter_words == ["abcd"]