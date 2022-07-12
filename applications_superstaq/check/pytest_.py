#!/usr/bin/env python3

import subprocess
import sys
import textwrap
from typing import Callable, Iterable, Optional, Union

from applications_superstaq.check import check_utils


@check_utils.enable_exit_on_failure
def run(
    *args: str,
    include: Union[str, Iterable[str]] = "*_test.py",
    exclude: Union[str, Iterable[str]] = "*_integration_test.py",
    notebook_include: Union[str, Iterable[str]] = "*.ipynb",
    notebook_exclude: Union[str, Iterable[str]] = "",
    integration_include: Union[str, Iterable[str]] = "*_integration_test.py",
    integration_exclude: Union[str, Iterable[str]] = "dev_tools/*",
    integration_setup: Optional[Callable] = None,
    silent: bool = False,
) -> int:

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

    if parsed_args.notebook:
        args_to_pass += ["--nbmake"]
        include = notebook_include
        exclude = notebook_exclude

    elif parsed_args.integration:
        if integration_setup:
            integration_setup()
        include = integration_include
        exclude = integration_exclude

    files = check_utils.get_file_args(parsed_args, include, exclude, silent)

    if not parsed_args.integration and not parsed_args.enable_socket:
        args_to_pass += ["--disable-socket"]

    return subprocess.call(["pytest", *files, *args_to_pass], cwd=check_utils.root_dir)


if __name__ == "__main__":
    exit(run(*sys.argv[1:]))
