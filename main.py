#!/usr/bin/env python
import os
import sys
import uuid
import copy
import struct
import argparse
from uefi_def import *
from guid import *
from fv import *
from ctypes import *
from var import *

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='commands')

    parser_genhdr = subparsers.add_parser('prase',  help='prase uefi bios fv')
    parser_genhdr.set_defaults(which='prase')
    parser_genhdr.add_argument('-f', dest='bin', type=str, help='BIOS binary file path', required = True)
    parser_genhdr.add_argument('-n', dest='fvName', type=str, help='fv name {NV/DXE/PEI}', required = True)

    parser_genhdr = subparsers.add_parser('var',  help='prase uefi bios')
    parser_genhdr.set_defaults(which='var')
    parser_genhdr.add_argument('-f', dest='bin', type=str, help='BIOS binary file path', required = True)
    args = parser.parse_args()
    if args.which == 'prase':
        bios = Fv (args.bin, args.fvName)
        v = sizeof(AUTH_VARIABLE_HEADER)
        v = 0x26
        v = (((~v) + 1) & (1 - 1))

        print v
    elif args.which == 'var':
        nv = Fv (args.bin, "NV")
        print nv.fvSize
        var = Variable (nv.fvBuffer, 0x1e000, 0x2000, 0x20000)
        var.findVariableAll()
    else:
        pass

    print 'Done!'
    return 0



if __name__ == '__main__':
    main()