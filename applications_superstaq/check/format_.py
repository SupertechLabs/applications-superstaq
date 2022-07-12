#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import textwrap
from typing import Optional

from applications_superstaq.check import check_utils

default_files_to_check = ("*.py", "*.ipynb")


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
        Runs black on the repository (formatting check).
        """
    )

    parser.add_argument("--apply", action="store_true", help="Apply changes to files.")
    parsed_args, args_to_pass = parser.parse_known_intermixed_args(args)
    files = parsed_args.files

    args_to_pass = ["--color", "--line-length=100"] + args_to_pass
    if not parsed_args.apply:
        args_to_pass = ["--diff", "--check"] + args_to_pass

    if not files:
        files = check_utils.get_tracked_files(*default_files_to_check)

    returncode = subprocess.call(["black", *files, *args_to_pass], cwd=check_utils.root_dir)

    if returncode == 1:
        # some files should be reformatted, but there don't seem to be any bona fide errors
        this_file = os.path.relpath(__file__)
        print(f"Run '{this_file} --apply' to format the files.")

    return returncode


if __name__ == "__main__":
    exit(run(*sys.argv[1:]))
