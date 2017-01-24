# -*- coding: utf-8 -*-
import os
import sys
import struct



FIRMWARE_VOLUME_GUIDS = {
    "NV":  "fff12b8d-7696-4c8b-a985-2747075b4f50",
}



class Guid:
    
    def __init__(self, guid):
        self.guid = guid

    def compareGuid(self, guid1):
        if self.guid == guid1:
            return True
        return False

    def sGuid(self):
        """
        This function changed guid to format like xxxxxxxx-xxxx-xxxx-xxxxxxxx
        learn from :https://github.com/theopolis/uefi-firmware-parser/blob/master/uefi_firmware/utils.py
        """
        if self.guid is None or len(self.guid) != 16:
            return ""
        a, b, c, d = struct.unpack("%sIHH8s" % ("<"), self.guid)
        d = ''.join('%02x' % ord(c) for c in d)
        return "%08x-%04x-%04x-%s-%s" % (a, b, c, d[:4], d[4:])