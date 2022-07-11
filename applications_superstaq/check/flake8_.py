#!/usr/bin/env python3

import argparse
import subprocess
import sys
import textwrap
from typing import Iterable, Optional

from applications_superstaq.check import check_utils

default_files_to_check = ("*.py",)


@check_utils.enable_exit_on_failure
@check_utils.enable_incremental(*default_files_to_check)
def run(
    *args: str,
    files: Optional[Iterable[str]] = None,
    parser: argparse.ArgumentParser = check_utils.get_file_parser(),
) -> int:

    parser.description = textwrap.dedent(
        """
        Runs flake8 on the repository (formatting check).
        """
    )

    parsed_args, args_to_pass = parser.parse_known_intermixed_args(args)
    files = parsed_args.files

    if not files:
        files = check_utils.get_tracked_files(*default_files_to_check)

    return subprocess.call(["flake8", *files, *args_to_pass], cwd=check_utils.root_dir)


if __name__ == "__main__":
    exit(run(*sys.argv[1:]))
