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

    parser_genhdr = subparsers.add_parser('var',  help='prase uefi bios variable')
    parser_genhdr.set_defaults(which='var')
    parser_genhdr.add_argument('-f', dest='bin', type=str, help='BIOS binary file path', required = True)
    parser_genhdr.add_argument('-vs', dest='vpdSize', type=int, help='vpd size of the variable', required = True)
    parser_genhdr.add_argument('-ws', dest='vpdWorkingSize', type=int, help='ftw working size of the variable', required = True)
    parser_genhdr.add_argument('-vn', dest='variableName', type=str, help='variable name', required = False, default="")
    args = parser.parse_args()
    if args.which == 'prase':
        bios = Fv (args.bin, args.fvName)

    elif args.which == 'var':
        nv = Fv (args.bin, "NV")
        print nv.fvSize
        if args.vpdSize + args.vpdWorkingSize > nv.fvSize:
            print "error size of variable !!"
            return 0
        var = Variable (nv.fvBuffer, args.vpdSize, args.vpdWorkingSize, nv.fvSize-args.vpdSize-args.vpdWorkingSize)
        if args.variableName.strip(): 
            var.findVariableByName(args.variableName)
        else:
            var.findVariableAll()
    else:
        pass

    print 'Done!'
    return 0



if __name__ == '__main__':
    main()