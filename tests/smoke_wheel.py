"""Check that the installed native executable starts and prints its greeting."""
import subprocess
import sys
from pathlib import Path

cli = str(Path(sys.argv[1]).resolve())
result = subprocess.run([cli], check=True, capture_output=True, text=True)
assert (result.stdout + result.stderr).strip() == "Hello, zig-cli-pypi-demo!!!"
print("Installed zypi-demo passed the command check.")
