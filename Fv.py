#!/usr/bin/env python
import os
import sys
import uuid
import copy
import struct
import argparse
from uefi_def import *
from guid import *

class Bios:
    def __init__(self, biosBin):
        self.bios = biosBin
        hfsp = open(self.bios, 'r+b')
        self.biosSize = os.path.getsize(self.bios)
        self.biosBuffer = bytearray(hfsp.read())
        hfsp.close()

    def findFvOffset(self, fvGuid):
        '''find the fv offset of the bios by fv guid'''
        for offset in range(0, self.biosSize, 4):
            fvh = EFI_FIRMWARE_VOLUME_HEADER.from_buffer(self.biosBuffer, offset)
            if '_FVH' == bytearray.fromhex('%08X' % fvh.Signature)[::-1]:         
                if Guid(fvh.FileSystemGuid).sGuid() == fvGuid:
                    print offset
                    return offset

class Fv(Bios):
    def __init__(self, bin, fvName):
        Bios.__init__(self, bin)
        self.fvGuid = FIRMWARE_VOLUME_GUIDS[fvName]
        self.fvName = fvName
        self.fvOffSetOfBios = Bios.findFvOffset(self, self.fvGuid)

        
    def fvNvPrase(self):
        pass

    def fvDxePrase(self):
        pass
    
    def fvPeiPrase(self):
        pass

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='commands')

    parser_genhdr = subparsers.add_parser('prase',  help='prase uefi bios')
    parser_genhdr.set_defaults(which='prase')
    parser_genhdr.add_argument('-f', dest='bin', type=str, help='BIOS binary file path', required = True)
    args = parser.parse_args()
    if args.which == 'prase':
        bios = Fv (args.bin, "NV")
    else:
        pass

    print 'Done!'
    return 0



if __name__ == '__main__':
    main()