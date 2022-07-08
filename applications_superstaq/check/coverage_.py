#!/usr/bin/env python3

import argparse
import subprocess
import sys
import textwrap
from typing import Iterable, Optional, Union

from applications_superstaq.check import check_utils

default_files_to_check = ("*.py",)
default_exclude = ("*_integration_test.py",)


@check_utils.enable_exit_on_failure
@check_utils.extract_file_args
@check_utils.enable_incremental(*default_files_to_check, exclude=default_exclude)
def run(
    *args: str,
    files: Optional[Iterable[str]] = None,
    parser: argparse.ArgumentParser = check_utils.get_file_parser(),
    suppress_warnings: bool = False,
    exclude: Optional[Union[str, Iterable[str]]] = default_exclude,
) -> int:

    parser.description = textwrap.dedent(
        """
        Checks to make sure that all code is covered by unit tests.
        Fails if any pytest fails or if coverage is not 100%.
        Ignores integration tests and files in the [repo_root]/examples directory.
        """
    )
    parser.parse_args(args)

    if files is None:
        files = check_utils.get_tracked_files(*default_files_to_check, exclude=exclude)
        suppress_warnings = True

    test_files = check_utils.get_test_files(*files, exclude=exclude, silent=suppress_warnings)

    if test_files:
        include_files = "--include=" + ",".join(files)
        test_returncode = subprocess.call(
            ["coverage", "run", *args, include_files, "-m", "pytest", *test_files],
            cwd=check_utils.root_dir,
        )

        coverage_returncode = subprocess.call(
            ["coverage", "report", "--precision=2"], cwd=check_utils.root_dir
        )

        if test_returncode:
            print(check_utils.failure("TEST FAILURE!"))
            exit(test_returncode)

        if coverage_returncode:
            print(check_utils.failure("COVERAGE FAILURE!"))
            exit(coverage_returncode)

        print(check_utils.success("TEST AND COVERAGE SUCCESS!"))

    else:
        print("No test files to check for pytest and coverage.")

    return 0


if __name__ == "__main__":
    exit(run(*sys.argv[1:]))
