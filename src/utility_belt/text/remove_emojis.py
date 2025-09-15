import re
import argparse
import unicodedata
import string

def remove_emojis_and_uncommon_symbols(text: str) -> str:
    """
    Remove emojis (including pictographs, transport symbols, flags, dingbats)
    and uncommon symbols, while preserving letters, digits, whitespace,
    and common ASCII punctuation.
    """
    cleaned_chars = []
    ascii_punct = set(string.punctuation)
    for char in text:
        cat = unicodedata.category(char)
        # Remove all symbol categories (S*) except ASCII punctuation
        if cat.startswith('S') and char not in ascii_punct:
            continue
        # Specifically remove other pictographic symbols (Emojis)
        # Emojis often fall under category 'So'
        if cat == 'So':
            continue
        cleaned_chars.append(char)
    return ''.join(cleaned_chars)


def main():
    # parser = argparse.ArgumentParser(
    #     description="Remove emojis and non-alphanumeric symbols from a text file."
    # )
    # parser.add_argument(
    #     "input_file",
    #     help="Path to the input .txt file",
    # )
    # parser.add_argument(
    #     "output_file",
    #     help="Path to the output cleaned .txt file",
    # )
    # args = parser.parse_args()

    input_file = r"C:\Users\keith\Downloads\enhanced_rha_system.txt"
    output_file = r"C:\Users\keith\Downloads\enhanced_rha_system_clean.txt"

    # Read the input file
    # with open(args.input_file, 'r', encoding='utf-8') as infile:
    with open(input_file, 'r', encoding='utf-8') as infile:
        content = infile.read()

    # Clean the content
    cleaned_content = remove_emojis_and_uncommon_symbols(content)

    # Write the cleaned content to the output file
    # with open(args.output_file, 'w', encoding='utf-8') as outfile:
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(cleaned_content)

    print(f"Cleaned content written to {output_file}")


if __name__ == "__main__":
    main()
