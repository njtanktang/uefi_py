import os
import sys
import uuid
import copy
import struct
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
                    return offset

class Fv(Bios):
    def __init__(self, bin, fvName):
        Bios.__init__(self, bin)
        self.fvGuid = FIRMWARE_VOLUME_GUIDS[fvName]
        self.fvName = fvName
        self.fvOffSetOfBios = Bios.findFvOffset(self, self.fvGuid)
        self.fvh = EFI_FIRMWARE_VOLUME_HEADER.from_buffer(self.biosBuffer, self.fvOffSetOfBios)
        self.fvSize = self.fvh.FvLength
        print (self.fvSize)
        self.fvBuffer = self.biosBuffer[self.fvOffSetOfBios : self.fvOffSetOfBios+self.fvSize]

    def getFvSize(self):
        return self.fvSize
    
    def getFvName(self):
        return self.fvName

    def fvNvPrase(self):
        pass

    def fvDxePrase(self):
        pass
    
    def fvPeiPrase(self):
        pass
