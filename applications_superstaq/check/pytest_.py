#!/usr/bin/env python3

import argparse
import subprocess
import sys
import textwrap
from typing import Callable, Iterable, Optional, Union

from applications_superstaq.check import check_utils

default_files_to_check = ("*.py",)
default_exclude = ("*_integration_test.py",)


@check_utils.enable_exit_on_failure
@check_utils.enable_incremental(*default_files_to_check, exclude=default_exclude)
def run(
    *args: str,
    exclude: Optional[Union[str, Iterable[str]]] = default_exclude,
    integration_exclude: Optional[Union[str, Iterable[str]]] = "dev_tools/*",
    integration_setup: Optional[Callable] = None,
    parser: Optional[argparse.ArgumentParser] = None,
) -> int:
    if not parser:
        parser = check_utils.get_file_parser()

    parser.description = textwrap.dedent(
        """
        Runs pytest on the repository.
        Ignores integration tests unless running in integration mode.
        """
    )

    # notebook and integration tests are mutually exclusive
    exclusive_group = parser.add_mutually_exclusive_group()
    exclusive_group.add_argument(
        "--notebook",
        action="store_true",
        help="Run pytest on all *.ipynb files in the repository.",
    )
    exclusive_group.add_argument(
        "--integration",
        action="store_true",
        help="Run pytest on all *integration_test.py files in the repository.",
    )

    parser.add_argument(
        "--enable-socket",
        action="store_true",
        help="Force-enable socket (i.e. do not pass --disable-socket to pytest). "
        + "Enabled automatically if running in integration mode.",
    )

    parsed_args, args_to_pass = parser.parse_known_intermixed_args(args)
    files = parsed_args.files

    if parsed_args.notebook:
        args_to_pass += ("--nbmake",)
        files = check_utils.get_tracked_files("**/*.ipynb", exclude=exclude)

    if parsed_args.integration:
        if integration_setup:
            integration_setup()

        if not files:
            files = check_utils.get_tracked_files(
                "*_integration_test.py", exclude=integration_exclude
            )

    elif not parsed_args.enable_socket:
        args_to_pass += ("--disable-socket",)

    if not files:
        tracked_files = check_utils.get_tracked_files(*default_files_to_check, exclude=exclude)
        files = check_utils.get_test_files(*tracked_files, exclude=exclude, silent=True)

    return subprocess.call(["pytest", *files, *args_to_pass], cwd=check_utils.root_dir)


if __name__ == "__main__":
    exit(run(*sys.argv[1:]))
