#!/usr/bin/env python3

import applications_superstaq

if __name__ == "__main__":
    exit(applications_superstaq.check.pylint_.run(*sys.argv[1:]))
