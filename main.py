#!/usr/bin/env python3

# TCRFactory: a Web Application for TCR Repertoire Sequencing.
# D. Malko
# 2021

import re
import argparse
import socket

from lib.inout import Bin, Log, Xmx
from lib.pipeline import MiSeqPipe, NextSeqPipe


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
    in_dir = re.sub(r'/$', '', args.i)
    out_dir = re.sub(r'/$', '', args.o) if args.o else args.o
    bin_dir = re.sub(r'/$', '', args.b) if args.b else args.b
    xmx_size = args.m
    log_file = args.l
    overseq = args.f
    collisions = args.c
    compressed = args.z
    remove_seq = args.r
    port = int(args.p)
    ini = int(args.n)
    seq_tool = args.t

    if port:  # open a socket connection to prevent running multiple instances of the script
        try:
            # create a TCP/IP socket
            my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # bind the socket to the port
            server_address = ('localhost', port)
            print('starting up on {} port {}'.format(*server_address))
            my_sock.bind(server_address)
        except socket.error:
            exit("can't start: an instance of the script is running or the port is taken\n")

    if not out_dir:
        out_dir = '/output' if in_dir == '/' else in_dir + '/output'
    elif out_dir in ('.', '..'):
        out_dir = out_dir + '/output'
    elif out_dir == '/':
        out_dir = '/output'

    Bin(bin_dir)
    Xmx(xmx_size)
    log = Log(log_file)

    pipe = None
    if seq_tool == 'MiSeq':
        pipe = MiSeqPipe(in_dir, out_dir)
        pipe.set_overseq(overseq)
        pipe.set_collisions(collisions)
    elif seq_tool == 'NextSeq':
        pipe = NextSeqPipe(in_dir, out_dir)

    if pipe:
        if not ini:
            pipe.check()
        pipe.execute(log)
    else:
        print('Wrong the pipeline. Aborted.')

    print('...done')

# end of main()


if __name__ == '__main__':
    main()

