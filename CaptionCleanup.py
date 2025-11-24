import argparse
import re

def remove_timestamp(input_file:str) -> None:
    """ Removes timestamps from a vtt file
        Args:
            input_file: the path to the Input File.
        Variables:
            regex_pattern: list of regex patterns to replace
            output_file: the path of the cleaned up file.
        Notes:
            This cmdlet can accept a --file Argument in a Batch file that points to a file location
                e.g.: --file="D:\\Path\\to\\File\\file.vtt" or --file=file.vtt if the File is in the same Directory.
                If no --file is provided, the cmdlet will prompt the user to supply the filepath.
            We assume that the Input file is a .vtt file. If this is not correct, you can change the 
                output_file extension below.
            We also assume the regex timestamp is in 00:00:00.000 --> 00:00:00.000 format
                and the additional regex strings are unique to the Storyline Generative Caption creation.
                I tried to make it as exclusionary as possible, so hopefully this will not catch "legitimate" Captions.
    """
    # 1. Patterns for metadata and timestamp lines to be removed
    regex_patterns:list = [
        r"WEBVTT",
        r"NOTE",
        r"Kind: captions",
        r"Source:(.*)",
        r"Source Version:(.*)",
        # Pattern to remove the timestamp line (HH:MM:SS.mmm --> HH:MM:SS.mmm)
        r"^\d{2}:\d{2}:\d{2}.\d{3} --> \d{2}:\d{2}:\d{2}.\d{3}"
    ]
    # 2. Define output file name
    output_file:str = input_file.replace('.vtt', '_Updated.vtt')
    try:
        with open(input_file, "r") as iFile, \
            open(output_file, "w") as oFile:
            for line in iFile:
                # Strip leading/trailing whitespace (including newline) for clean checks
                stripped_line:str = line.strip()
                # Filter 1: Check for empty/blank lines (after stripping whitespace)
                if not stripped_line:
                    continue # Skip to the next line if the line is empty or only whitespace
                # Filter 2: Check against regex patterns
                matched:bool = False
                for pattern in regex_patterns:
                    if re.search(pattern, line):
                        matched = True
                        break
                # If the line is not empty AND not matched by a regex pattern, write it.
                if not matched:
                    # Write the stripped line followed by a newline character.
                    # This ensures the output is tightly packed but still legible, 
                    # and avoids writing extra blank lines.
                    oFile.write(line)
        print(f"Caption file {output_file} was succesfully updated!")
    except FileNotFoundError:
        print(f"File not found: {input_file}")
    except Exception as e:
        print(f"An Error has occurred: {e}")

if __name__ == "__main__":
    input_file:str = ''
    parser:argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=None, help='Filepath to the Caption file')
    args:argparse.Namespace = parser.parse_args()
    if not (args.file is None):
        input_file = args.file        
    else:
        # no File was given, so prompt the user
        input_file = input("Enter the Caption file to be updated, including FilePath: ")
    remove_timestamp(input_file)