#!/usr/bin/env python3

import sys

import applications_superstaq.check as check

if __name__ == "__main__":
    exit(check.format_.run(*sys.argv[1:]))
