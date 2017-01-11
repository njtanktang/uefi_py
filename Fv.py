#!/usr/bin/env python
import os
import sys
import uuid
import copy
import struct
import argparse
from   ctypes import *
"""
EFI_FIRMWARE_VOLUME_HEADER is define at uefi pi spec vol3,
3.2.1 Firmware volume
typedef struct {
  UINT8                 ZeroVector[16];
  EFI_GUID              FileSystemGuid;
  UINT64                FvLength;
  UINT32                Signature;
  EFI_FVB_ATTRIBUTES_2  Attributes;
  UINT16                HeaderLength;
  UINT16                Checksum;
  UINT16                ExtHeaderOffset;
  UINT8                 Reserved[1];
  UINT8                 Revision;
  EFI_FV_BLOCK_MAP      BlockMap[];
} EFI_FIRMWARE_VOLUME_HEADER;
"""
class EFI_FIRMWARE_VOLUME_HEADER(Structure):
    _fields_ = [
        ('ZeroVector',                 ARRAY(c_uint8, 16)),
        ('FileSystemGuid',             ARRAY(c_char, 16)),
        ('FvLength',                   c_uint64),
        ('Signature',                  c_uint32),
        ('Attributes',                 c_uint32),
        ('HeaderLength',               c_uint16),
        ('Checksum',                   c_uint16),
        ('ExtHeaderOffset',            c_uint16),
        ('Reserved',                   c_uint8),
        ('Revision',                   c_uint8)
        ]

class Bios:
    def __init__(self, bios_bin):
        self.fv = bios_bin
        hfsp = open (self.fv, 'r+b')
        self.size = os.path.getsize (self.fv)
        self.buffer = bytearray(hfsp.read())
        hfsp.close()

    def find_header(self):
        for offset in range(0, self.size, 1) :
            fvh = EFI_FIRMWARE_VOLUME_HEADER.from_buffer(self.buffer, offset)
            if '_FVH' == bytearray.fromhex('%08X' % fvh.Signature)[::-1] :
                return offset

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='commands')

    parser_genhdr = subparsers.add_parser('prase',  help='prase uefi bios')
    parser_genhdr.set_defaults(which='prase')
    parser_genhdr.add_argument('-f', dest='bin', type=str, help='BIOS binary file path', required = True)
    args = parser.parse_args()
    if args.which == 'prase':
        bios = Bios (args.bin)
        bios.find_header()
    else:
        pass

    print 'Done!'
    return 0



if __name__ == '__main__':
    main()