# -*- coding: utf-8 -*-
import os
import sys
import struct



FIRMWARE_VOLUME_GUIDS = {
    "NV":  "fff12b8d-7696-4c8b-a985-2747075b4f50",
}

VARIABLE_SIGN_GUID = {
    "Variable":        "ddcf3616-3275-4146-98b6-fe85707ffe7d",
    "Authenticated":    "515fa686-b06e-4550-9112-382bf1067bfb",
    "Auth_based_time":  "aaf32c78-947b-439a-a180-2e144ec37792",
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