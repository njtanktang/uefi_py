import os
import sys
import uuid
import copy
import struct
from uefi_def import *


class Variable(self, variableName, vendorGuid, variableBuffer):

    def __init__(self, variableName, vendorGuid, variableBuffer):
        self.name = variableName
        self.guid = vendorGuid
        self.buffer = variableBuffer
        self.fvh = EFI_FIRMWARE_VOLUME_HEADER.from_buffer(self.buffer, 0)
    def check_variable_store_status(self):
        
    def find_variable_header(self):

