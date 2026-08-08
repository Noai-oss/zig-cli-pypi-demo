# Portions derived from Ruff: https://github.com/astral-sh/ruff/tree/6f86de2eb6363f77a314998c414ac8b53849b92f/python/ruff
# Copyright (c) 2022 Charles Marsh
# SPDX-License-Identifier: MIT

import os
import sys

from zypi_demo import find_zypi_demo_bin


def _run() -> None:
    zypi_demo = find_zypi_demo_bin()

    if sys.platform == "win32":
        import subprocess

        try:
            completed_process = subprocess.run([zypi_demo, *sys.argv[1:]], check=False)
        except KeyboardInterrupt:
            sys.exit(2)

        sys.exit(completed_process.returncode)
    else:
        os.execvp(zypi_demo, [zypi_demo, *sys.argv[1:]])


if __name__ == "__main__":
    _run()
