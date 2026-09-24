"""This script removes timestamps and metadata from .vtt and .srt caption files
   created by Storyline Generative Captions."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
from typing import Union

# Pre-compiled patterns for metadata and timestamp lines to be removed
CLEANUP_PATTERNS: list[re.Pattern[str]] = [
    # Header level Patterns at the start of the Caption
    re.compile(r"WEBVTT"),
    re.compile(r"NOTE"),
    re.compile(r"Kind: captions"),
    re.compile(r"^(Source(?: Version)?: )\s*(.+)$"),
    # SRT numeric cue identifiers
    re.compile(r"^\d+$"),
    # Timestamp Pattern: HH:MM:SS.mmm --> HH:MM:SS.mmm (supports '.' and ',')
    re.compile(r"^\d{2}:\d{2}:\d{2}[.,]\d{3} --> \d{2}:\d{2}:\d{2}[.,]\d{3}"),
]

def remove_timestamp(input_path: Union[str, Path]) -> None:
    """Removes timestamps and metadata from a .vtt or .srt caption file.
    Args:
        input_path: The path to the input caption file (str or Path).
    """
    input_path = Path(input_path)
    if not input_path.name:
        print("Error: No file path provided.")
        return

    output_file: Path = input_path.with_stem(f"{input_path.stem}_Updated")

    try:
        with open(input_path, "r", encoding="utf-8-sig") as in_file, \
             open(output_file, "w", encoding="utf-8") as out_file:
            for line in in_file:
                # Skip empty lines and lines matching metadata/timestamp patterns
                if line.strip() and not any(p.search(line) for p in CLEANUP_PATTERNS):
                    out_file.write(line)
        print(f"Caption file {output_file} was successfully updated!")
    except FileNotFoundError:
        print(f"File not found: {input_path}")
    except IsADirectoryError:
        print(f"Expected a file but found a directory: {input_path}")
    except PermissionError:
        print(
            "Permission denied when accessing the file(s). "
            f"Check read/write permissions for: {input_path} or {output_file}"
        )
    except UnicodeDecodeError:
        print(
            "Could not decode file using UTF-8. "
            f"Try a different encoding or clean the file: {input_path}"
        )
        output_file.unlink(missing_ok=True)
    except OSError as os_err:
        print(f"I/O error while reading or writing files: {os_err}")
        output_file.unlink(missing_ok=True)

def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Clean caption files by removing timestamps and Storyline metadata."
    )
    parser.add_argument(
        '--file', type=str, default=None,
        help='Path to the Caption file. Can be absolute or relative. '
             'If not provided, the user will be prompted.'
    )
    args = parser.parse_args()
    raw_input = args.file or input("Enter the Path to the Caption file to be updated: ")
    input_file = raw_input.strip().strip("'\"")
    if not input_file:
        print("Error: No file path provided.")
        return
    remove_timestamp(input_file)

if __name__ == "__main__":
    main()
