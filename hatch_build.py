import os
import subprocess
from pathlib import Path
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from packaging.tags import sys_tags

CLI_NAME = "zypi-demo"
CLI_NAME_UPPER = CLI_NAME.replace("-", "_").upper()


class CustomBuildHook(BuildHookInterface):
    """Build Zig and put the executable in the wheel's scripts directory."""

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        zig_target = os.getenv(f"{CLI_NAME_UPPER}_ZIG_TARGET")
        wheel_tag = os.getenv(f"{CLI_NAME_UPPER}_WHEEL_TAG")

        # NOTE: Requiring both values prevents the compiled target and the
        # compatibility tag advertised by the wheel from diverging.
        if bool(zig_target) != bool(wheel_tag):
            raise RuntimeError(
                f"{CLI_NAME_UPPER}_ZIG_TARGET and {CLI_NAME_UPPER}_WHEEL_TAG must either both be set or both be unset"
            )

        command = ["zig", "build", "-Doptimize=ReleaseSmall"]
        if zig_target:
            command.append(f"-Dtarget={zig_target}")

        subprocess.run(command, cwd=self.root, check=True)

        # NOTE: Cross-builds choose the executable suffix from the target OS;
        # local builds fall back to the host OS.
        target_is_windows = "windows" in zig_target if zig_target else os.name == "nt"
        binary_name = f"{CLI_NAME}.exe" if target_is_windows else CLI_NAME
        binary = Path(self.root, "zig-out", "bin", binary_name)
        if not binary.is_file():
            raise FileNotFoundError(
                f"Zig did not produce the expected binary: {binary}"
            )
        if binary.suffix != ".exe":
            # NOTE: This works on Unix hosts. Windows-hosted Unix wheels get
            # their POSIX execute bits repaired by make_wheels.py.
            binary.chmod(binary.stat().st_mode | 0o111)

        build_data["pure_python"] = False
        # NOTE: Cross-builds supply an explicit tag; local builds derive the
        # current interpreter's platform tag.
        build_data["tag"] = wheel_tag or f"py3-none-{next(iter(sys_tags())).platform}"

        # NOTE: shared_scripts installs the native binary into the environment's
        # scripts directory rather than inside the importable Python package.
        source = binary.relative_to(self.root).as_posix()
        build_data["shared_scripts"][source] = binary_name
