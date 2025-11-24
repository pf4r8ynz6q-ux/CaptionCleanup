# CaptionCleanup
CaptionCleanup is a small Python utility that cleans WebVTT (.vtt) caption files by removing timestamp lines
and common Articulate/Storyline-generated metadata. It produces a compact, human-readable caption file
that is easier to review or repurpose for documentation and transcripts.

## Features
- Removes WebVTT header lines such as `WEBVTT` and `NOTE` blocks
- Removes Storyline/Articulate metadata lines like `Kind: captions`, `Source: ...`, and `Source Version: ...`
- Removes timestamp lines in the format `HH:MM:SS.mmm --> HH:MM:SS.mmm`
- Skips blank lines so the output is tightly packed and readable

## Requirements
- Python 3.7+

## Installation
No external dependencies are required. Clone or download this repository and run the script with Python.

Example (PowerShell):

```powershell
python CaptionCleanup.py --file "AddingGotoAction.vtt"
```

Or run without the `--file` argument and you will be prompted to enter the caption file path:

```powershell
python CaptionCleanup.py
# Enter the Caption file to be updated, including FilePath: D:\path\to\file.vtt
```

## Usage
- Provide a `.vtt` file using the `--file` argument or when prompted interactively.
- The cleaned file will be written to the same directory with `_Updated.vtt` appended to the input filename
	(for example `AddingGotoAction.vtt` -> `AddingGotoAction_Updated.vtt`).

### Example
Run the script against the included sample file:

```powershell
python CaptionCleanup.py --file "AddingGotoAction.vtt"
# Output: Caption file AddingGotoAction_Updated.vtt was succesfully updated!
```

## Notes & Behavior
- The script uses a fixed set of regular expressions to remove header/metadata and timestamp lines. Current patterns include:
	- `WEBVTT`
	- `NOTE`
	- `Kind: captions`
	- `Source:(.*)`
	- `Source Version:(.*)`
	- Timestamp pattern `HH:MM:SS.mmm --> HH:MM:SS.mmm`
- The patterns are intended to be conservative for Storyline-generated captions; if your captions contain
	legitimate caption text that matches these patterns, edit `CaptionCleanup.py` to adjust or remove patterns.
- If the input file is not found, the script prints a `File not found` message.

## Batch / Automation
You can call the script from batch files or other automation tools. An example batch wrapper is included in the
repository (`__CaptionCleanup.bat`) for Windows automation scenarios.

## Contributing
This is a small utility. If you find issues or want additional filtering patterns, open an issue or submit a pull request.

## License
This repository does not include an explicit license. If you plan to reuse or distribute this tool, consider adding
a license file (for example MIT) to clarify reuse terms.

---
If you want, I can also: add a `requirements.txt` (not needed currently), add example input/output files, or
update `CaptionCleanup.py` to accept directory inputs and process multiple files. Which would you prefer next?
