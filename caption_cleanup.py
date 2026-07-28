"""This script removes timestamps and metadata from a .vtt caption file
   created by Storyline Generative Captions."""
import argparse
import re

def remove_timestamp(filepath: str) -> None:
    """
        Args:
            filepath: the path to the Input File.
        Variables:
            regex_pattern: list of regex patterns to replace
            output_file: the path of the cleaned up file.
        Notes:
            This cmdlet can accept a --file Argument in a Batch file that points to a file location
                e.g.: --file="D:\\Path\\to\\File\\file.vtt" or --file=file.vtt if local.
                If no --file is provided, the cmdlet will prompt the user to supply the filepath.
            We assume that the Input file is a .vtt file.
            We also assume the regex timestamp is in 00:00:00.000 --> 00:00:00.000 format
                and the additional regex strings are unique to the Storyline Generative Caption.
                Proofreading the end results is highly encouraged.
    """
    # 1. Patterns for metadata and timestamp lines to be removed
    regex_patterns: list = [
        # Header level Patterns at the start of the Caption
        r"WEBVTT",
        r"NOTE",
        r"Kind: captions",
        r"^(Source(?: Version)?: )\s*(.+)$",
        # Timestamp Pattern: HH:MM:SS.mmm --> HH:MM:SS.mmm
        r"^\d{2}:\d{2}:\d{2}.\d{3} --> \d{2}:\d{2}:\d{2}.\d{3}"
    ]
    # 2. Define output file name
    output_file: str = filepath.replace('.vtt', '_Updated.vtt')

    # 3. Pre-compile regex patterns and handle regex compilation errors
    try:
        compiled_patterns = [re.compile(p) for p in regex_patterns]
    except re.error as rex:
        print(f"Regex compilation error: {rex}")
        return

    # 4. Open files and process lines with more granular exception handling
    try:
        with open(filepath, "r", encoding="utf-8") as in_file, \
             open(output_file, "w", encoding="utf-8") as out_file:
            for line in in_file:
                # Skip empty lines and lines matching metadata/timestamp patterns
                if line.strip() and not any(p.search(line) for p in compiled_patterns):
                    out_file.write(line)
        print(f"Caption file {output_file} was succesfully updated!")
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except IsADirectoryError:
        print(f"Expected a file but found a directory: {filepath}")
    except PermissionError:
        print(f"Permission denied when accessing the file(s). "
              f"Check read/write permissions for: {filepath} or {output_file}")
    except UnicodeDecodeError:
        print(f"Could not decode file using UTF-8. "
              f"Try a different encoding or clean the file: {filepath}")
    except OSError as os_err:
        # Catch other OS-related errors (e.g., disk full, I/O errors)
        print(f"I/O error while reading or writing files: {os_err}")

def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=None,
                        help='Path to the Caption file. Can be absolute or relative. '
                             'If not provided, the user will be prompted.')
    args = parser.parse_args()
    input_file = args.file or input("Enter the Path to the Caption file to be updated: ")
    remove_timestamp(input_file)

if __name__ == "__main__":
    main()
