import os
import sys
import uuid
import copy
import struct
from uefi_def import *
from guid import *
from ctypes import *
# -*- coding: utf-8 -*-


class Variable:

    def __init__(self, fvNvBuffer, vpdSize, vpdWorkingSize, vpdSpareSize):

        self.vpdFvh = EFI_FIRMWARE_VOLUME_HEADER.from_buffer(fvNvBuffer, 0)
        self.vpdSize = self.vpdFvh.FvLength
        if self.vpdSize != vpdSize + vpdWorkingSize + vpdSpareSize:
            print "error length of variable region, pls check your binary"
            return

        self.vBuf  = fvNvBuffer[0 : vpdSize]
        self.vSize = vpdSize
        self.vwBuf = fvNvBuffer[vpdSize : (vpdSize+vpdWorkingSize)]
        self.vwSize = vpdWorkingSize
        self.vsBuf = fvNvBuffer[(vpdSize+vpdWorkingSize) : self.vpdSize]
        self.vsSize = vpdSpareSize
        '''we assume none athu variable as default'''
        self.athu = False 
        self.vsh = VARIABLE_STORE_HEADER.from_buffer(self.vBuf, self.vpdFvh.HeaderLength)
        if Guid(self.vsh.Signature).sGuid() not in VARIABLE_SIGN_GUID.values():
            print "error signature if variable region"
            return
        for (k,v) in VARIABLE_SIGN_GUID.items():
            if  Guid(self.vsh.Signature).sGuid() == v:
                if k != "Variable":
                    self.athu = True
        '''variable struct >>>>>>'''
        self.variableName = ""
        self.variableNameSize = 0
        self.variableData = []
        self.variableDataSize = 0
        self.variableGuid = ""
        '''variable struct <<<<<<'''

    def isValidVariable(self, var):
        '''if start id != 0x55aa, return error'''
        if var.StartId != VARIABLE_DATA:
            return False
        else:
            return True

    def dataSizeOfVariable(self, var):
        if var.State == 0xff or var.DataSize == 0xffffffff or var.NameSize == 0xffffffff or var.Attributes == 0xffffffff:
            return 0
        else:
            return var.DataSize

    def varNameSizeOfVariable(self, var):
        if var.State == 0xff or var.DataSize == 0xffffffff or var.NameSize == 0xffffffff or var.Attributes == 0xffffffff:
            return 0
        else:
            return var.NameSize

    def align(self, alignmemt, v):
        if alignmemt == 1:
            return 0
        else:
            return (((~v) + 1) & (alignmemt - 1))

    def printVar(self, varName, varData, varNameSize, varDataSize, varGuid):
        '''print  variable Name'''
        print "========================Start======================="
        vNameUni = struct.unpack(">%dH"%(varNameSize/2), varName)
        vNameAsc = []
        for s in range(0,len(vNameUni),1):
            vNameAsc.append(chr(vNameUni[s]>>8))
        print "variable Name: %s" % ''.join(vNameAsc)
        print varGuid
        '''print data vaule'''
        if varDataSize <= 4:
            print "variable data size: 0x%x" % varDataSize
            data = struct.unpack(">%dB"%varDataSize, varData)
            print data
        else:
            print "Variable DataSize = %x >> 4, don't print" % varDataSize 
        print "========================end======================="
        print ""
        
    def findVariable(self, varAddr):
        '''variable header'''
        if self.athu:
            var = AUTH_VARIABLE_HEADER.from_buffer(self.vBuf, varAddr)
        else:
            var = VARIABLE_HEADER.from_buffer(self.vBuf, varAddr)
        
        '''check if it is a normal variable'''
        
        if self.isValidVariable(var):
            if (var.State == 0x3f):
                varDataSize = self.dataSizeOfVariable(var)
                varNameSize = self.varNameSizeOfVariable(var)
                if self.athu:
                    varNameOffSet = varAddr + sizeof(AUTH_VARIABLE_HEADER)
                    varDataOffSet = varAddr + sizeof(AUTH_VARIABLE_HEADER) + varNameSize + self.align(1,varNameSize)     
                else:
                    varNameOffSet = varAddr + sizeof(AUTH_VARIABLE_HEADER)
                    varDataOffSet = varAddr + sizeof(VARIABLE_HEADER) + varNameSize + self.align(1,varNameSize)
                varName = self.vBuf[varNameOffSet : (varNameOffSet + varNameSize)]
                varData = self.vBuf[varDataOffSet : (varDataOffSet + varDataSize)]
                self.variableName = varName
                self.variableNameSize = varNameSize
                self.variableData = varData
                self.variableDataSize = varDataSize
                self.variableGuid = Guid(var.VendorGuid).sGuid()
               # self.printVar(varName, varData, varNameSize, varDataSize)
                return True
            else:
                return False

    def findNextVariable(self, varAddr):
        v = varAddr
        if self.athu:
            var = AUTH_VARIABLE_HEADER.from_buffer(self.vBuf, varAddr)
            v += sizeof(AUTH_VARIABLE_HEADER)
        else:
            var = VARIABLE_HEADER.from_buffer(self.vBuf, varAddr)
            v += sizeof(VARIABLE_HEADER)
        if self.isValidVariable(var) == False:
            return 0
            
        v += self.varNameSizeOfVariable(var)
        v += self.align(1, self.varNameSizeOfVariable(var))
        v += self.dataSizeOfVariable(var)
        v += self.align(1, self.dataSizeOfVariable(var))
        return  ((v + 4 - 1) & (~(4 - 1)))

    def cmpVarName(self, varName):
        vNameUni = struct.unpack(">%dH"%(self.variableNameSize/2), self.variableName)
        vNameAsc = []
        for s in range(0,len(vNameUni)-1,1):
            vNameAsc.append(chr(vNameUni[s]>>8))
        varNameCmp = ''.join(vNameAsc)
        if varNameCmp == varName:
            return True
        else:
            return False

    def findVariableAll(self):
        varAddr = self.vpdFvh.HeaderLength + sizeof(VARIABLE_STORE_HEADER)
        while  varAddr < self.vSize:
            if self.findVariable(varAddr):
                self.printVar(self.variableName, self.variableData, self.variableNameSize, self.variableDataSize,\
                self.variableGuid)
            varAddr = self.findNextVariable(varAddr)
            if varAddr == 0:
                break
     
    def findVariableByName(self, variableName):
        varAddr = self.vpdFvh.HeaderLength + sizeof(VARIABLE_STORE_HEADER)
        while  varAddr < self.vSize:
            if self.findVariable(varAddr):
                if self.cmpVarName(variableName):
                    self.printVar(self.variableName, self.variableData, self.variableNameSize, self.variableDataSize,\
                    self.variableGuid)
            varAddr = self.findNextVariable(varAddr)
            if varAddr == 0:
                break

