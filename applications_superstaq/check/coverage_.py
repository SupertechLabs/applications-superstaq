#!/usr/bin/env python3

import subprocess
import sys
import textwrap
from typing import Iterable, Union

from applications_superstaq.check import check_utils


@check_utils.enable_exit_on_failure
def run(
    *args: str,
    include: Union[str, Iterable[str]] = "*.py",
    exclude: Union[str, Iterable[str]] = "*_integration_test.py",
    silent: bool = False,
) -> int:

    parser = check_utils.get_file_parser()
    parser.description = textwrap.dedent(
        """
        Checks to make sure that all code is covered by unit tests.
        Fails if any pytest fails or if coverage is not 100%.
        Ignores integration tests and files in the [repo_root]/examples directory.
        """
    )

    parsed_args, args_to_pass = parser.parse_known_intermixed_args(args)
    files = check_utils.get_file_args(parsed_args, include, exclude, silent)

    silent = silent or not (parsed_args.files or parsed_args.revisions)
    test_files = check_utils.get_test_files(*files, exclude=exclude, silent=silent)

    if test_files:
        include_files = "--include=" + ",".join(files)
        test_returncode = subprocess.call(
            ["coverage", "run", include_files, *args_to_pass, "-m", "pytest", *test_files],
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
