# Subalive

Subalive is a Python script that checks the availability of subdomains listed in a text file and saves the alive subdomains to another text file.

## Usage

python subalive.py target.txt -o output.txt -rm


- `target.txt`: Input file containing subdomains to check.
- `-o output.txt`: (Optional) Output file to save alive subdomains. If not provided, default filename is "alive.txt".
- `-rm`: (Optional) to remove redirection 3xx.
- `-subdir`: (Optional) to avoid redirections to a subdirectory.
- `-https` : for https only
- `-http` : for http only
## Requirements

- Python 3.x
- requests module (install via `pip install requests`)

## Example

Check the availability of subdomains listed in `subdomains.txt` and save alive subdomains to `alive.txt`:

## Credits

script by kalendra456.
