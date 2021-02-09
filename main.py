#!/usr/bin/env python3

# TCRFactory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

import os
import re
import sys
import glob
import argparse

from lib.tools import Bin, ToolChecker, VDJtools


# It requires R packages: ggplot2, reshape

def main():
    bin_dir = Bin('tmp')
    checker = ToolChecker(bin_dir)

    status = checker.check_tools([VDJtools])
    if status:
        exit(status)

    vdj = VDJtools()

    input_parser = argparse.ArgumentParser(description='TCRFactory: a Web Application for TCR Repertoire Sequencing.')


if __name__ == '__main__':
    main()
