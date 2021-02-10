#!/usr/bin/env python3

# TCRFactory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

import os
import re
import sys
import glob
import argparse

from lib.tools import Bin, Log, Xmx, ToolChecker, VDJtools, Mixcr, Migec


# The script requires R packages: ggplot2, reshape
def main():
    input_parser = argparse.ArgumentParser(description='TCRFactory: a Web Application for TCR Repertoire Sequencing.')

    input_parser.add_argument('-t',
                              metavar='MiSeq',
                              choices=['MiSeq', 'NextSeq'],
                              help='the sequencing tool',
                              required=True)
    input_parser.add_argument('-i',
                              metavar='/path/to/input_dir',
                              help='the path to the input directory (the directory has to have a SampleInfo file)',
                              required=True)
    input_parser.add_argument('-o',
                              metavar='/path/to/output_dir',
                              default=None,
                              help='the path to the output directory',
                              required=False)
    input_parser.add_argument('-m',
                              metavar='6G',
                              default='6G',
                              help='Xmx memory size',
                              required=False)
    input_parser.add_argument('-f',
                              metavar='threshold_value',
                              default=0,
                              help='force overseq threshold',
                              required=False)
    input_parser.add_argument('-b',
                              metavar='/path/to/bin',
                              default=None,
                              help='the global path to a bin directory with the programs',
                              required=False)
    input_parser.add_argument('-l',
                              metavar='/path/to/file_name.log',
                              default=None,
                              help='the log file',
                              required=False)
    input_parser.add_argument('-z',
                              metavar='/path/to/file_name.tar.gz',
                              default=None,
                              help='the compressed file',
                              required=False)
    input_parser.add_argument('-p',
                              metavar='10000',
                              default=0,
                              help='a socket port number to prevent running multiple instances',
                              required=False)
    input_parser.add_argument('-c',
                              action='store_true',
                              help='force collision filter',
                              required=False)
    input_parser.add_argument('-r',
                              action='store_true',
                              help='remove sequence files from output',
                              required=False)
    input_parser.add_argument('-n',
                              action='store_true',
                              help='initialized (use if all required tools are installed)',
                              required=False)

    args = input_parser.parse_args()
    in_dir = re.sub(r'\/$', '', args.i)
    out_dir = re.sub(r'\/$', '', args.o) if args.o else args.o
    bin_dir = re.sub(r'\/$', '', args.b) if args.b else args.b
    xmx_size = args.m
    log_file = args.l
    overseq = args.f
    collisions = args.c
    compressed = args.z
    remove_seq = args.r
    port = int(args.p)
    ini = int(args.n)
    seq_tool = args.t

    tbin = Bin(bin_dir)
    log = Log(log_file)
    xmx = Xmx(xmx_size)
    if not ini:  # Check and install the missing tools
        print('NOTE: The script requires R packages: ggplot2, reshape. Check whether they are installed.')
        checker = ToolChecker(tbin)
        checker.check_tools([VDJtools, Mixcr, Migec])

    pass




if __name__ == '__main__':
    main()
