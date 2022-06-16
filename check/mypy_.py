#!/usr/bin/env python3

import sys

from applications_superstaq import check

if __name__ == "__main__":
    exit(check.mypy_.run(*sys.argv[1:]))
