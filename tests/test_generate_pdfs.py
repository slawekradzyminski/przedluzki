import pytest
from pathlib import Path
from src.generate_pdfs import parse_extensions_line


@pytest.fixture
def sample_extensions_file(tmp_path):
    # given
    extensions_file = tmp_path / "test_extensions.txt"
    with open(extensions_file, "w", encoding="utf-8") as f:
        # Real examples from the file
        f.write(" AAA \n")                         # No extensions
        f.write("B,L,Ł,Ż ABO \n")                 # Left extensions only
        f.write("B,C,D,L,P,R,T,Ł,Ż ABY M,Ś\n")   # Both extensions
        f.write("B,D,F,G,L,M,P,W,Ł ACH A,Y\n")    # Both extensions
        f.write("B,D,G,H,P,R,Z ACZ \n")           # Left extensions only
    return extensions_file


def test_parse_extensions_real_format(sample_extensions_file):
    # given
    with open(sample_extensions_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # when/then - test each line
    # Test case: " AAA " - No extensions
    left_ext, word, right_ext = parse_extensions_line(lines[0], word_length=3)
    assert left_ext == ""
    assert word == "AAA"
    assert right_ext == ""
    
    # Test case: "B,L,Ł,Ż ABO " - Left extensions only
    left_ext, word, right_ext = parse_extensions_line(lines[1], word_length=3)
    assert left_ext == "B,L,Ł,Ż"
    assert word == "ABO"
    assert right_ext == ""
    
    # Test case: "B,C,D,L,P,R,T,Ł,Ż ABY M,Ś" - Both extensions
    left_ext, word, right_ext = parse_extensions_line(lines[2], word_length=3)
    assert left_ext == "B,C,D,L,P,R,T,Ł,Ż"
    assert word == "ABY"
    assert right_ext == "M,Ś"
    
    # Test case: "B,D,F,G,L,M,P,W,Ł ACH A,Y" - Both extensions
    left_ext, word, right_ext = parse_extensions_line(lines[3], word_length=3)
    assert left_ext == "B,D,F,G,L,M,P,W,Ł"
    assert word == "ACH"
    assert right_ext == "A,Y"
    
    # Test case: "B,D,G,H,P,R,Z ACZ " - Left extensions only
    left_ext, word, right_ext = parse_extensions_line(lines[4], word_length=3)
    assert left_ext == "B,D,G,H,P,R,Z"
    assert word == "ACZ"
    assert right_ext == ""


def test_parse_extensions_word_length_validation(tmp_path):
    # given
    test_line = "B,C TOOLONG A,B"   # Too long word
    
    # when
    left_ext, word, right_ext = parse_extensions_line(test_line, word_length=3)
    
    # then
    assert word == ""  # Should return empty strings when word length doesn't match
    assert left_ext == ""
    assert right_ext == ""


def test_extensions_match_words_order():
    # given
    words_file = Path("slowniki/osps/3_letter_words.txt")
    extensions_file = Path("slowniki/osps/extensions/3_letter_extensions.txt")
    
    # when
    with open(words_file, "r", encoding="utf-8") as f:
        words = [line.strip().lower() for line in f if line.strip()]
    
    with open(extensions_file, "r", encoding="utf-8") as f:
        extensions = [parse_extensions_line(line, word_length=3) for line in f if line.strip()]
    extension_words = [word.lower() for _, word, _ in extensions if word]
    
    # then
    assert extension_words == words, "Words in extensions file do not match order in words file" 