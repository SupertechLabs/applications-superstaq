#!/usr/bin/env python3

import argparse
import subprocess
import sys
import textwrap
from typing import Optional

from applications_superstaq.check import check_utils

default_files_to_check = ("*.py",)


@check_utils.enable_exit_on_failure
@check_utils.enable_incremental(*default_files_to_check)
def run(
    *args: str,
    parser: Optional[argparse.ArgumentParser] = None,
) -> int:
    if not parser:
        parser = check_utils.get_file_parser()

    parser.description = textwrap.dedent(
        """
        Runs pylint on the repository (formatting check).
        NOTE: Only checks incrementally changed files by default.
        """
    )

    parser.add_argument("-a", "--all", action="store_true", help="Run pylint on the entire repo.")
    parsed_args, args_to_pass = parser.parse_known_intermixed_args(args)
    files = parsed_args.files

    if parsed_args.all:
        files += check_utils.get_tracked_files(*default_files_to_check)

    if not files:
        files = check_utils.get_changed_files(*default_files_to_check)

    return subprocess.call(["pylint", *files, *args_to_pass], cwd=check_utils.root_dir)


if __name__ == "__main__":
    exit(run(*sys.argv[1:]))
