
import ctypes

uint8_t = ctypes.c_ubyte
char = ctypes.c_char
uint32_t = ctypes.c_uint
uint64_t = ctypes.c_uint64
uint16_t = ctypes.c_ushort
guid_t = char * 16
efi_time = char * 16
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
class EFI_FIRMWARE_VOLUME_HEADER(ctypes.LittleEndianStructure):
    _fields_ = [
        ('ZeroVector',                 guid_t),
        ('FileSystemGuid',             guid_t),
        ('FvLength',                   uint64_t),
        ('Signature',                  uint32_t),
        ('Attributes',                 uint32_t),
        ('HeaderLength',               uint16_t),
        ('Checksum',                   uint16_t),
        ('ExtHeaderOffset',            uint16_t),
        ('Reserved',                   uint8_t),
        ('Revision',                   uint8_t)
        ]

"""
===========================================================================
define for uefi nvram
===========================================================================
"""
"""
#define VARIABLE_DATA                     0x55AA

//
// Variable Store Header flags
//
#define VARIABLE_STORE_FORMATTED          0x5a
#define VARIABLE_STORE_HEALTHY            0xfe
"""
VARIABLE_DATA = 0x55aa
VARIABLE_STORE_FORMATTED = 0x5a
VARIABLE_STORE_HEALTHY = 0xfe
"""
///
/// Variable Store region header.
///
typedef struct {
  ///
  /// Variable store region signature.
  ///
  EFI_GUID  Signature;
  ///
  /// Size of entire variable store, 
  /// including size of variable store header but not including the size of FvHeader.
  ///
  UINT32  Size;
  ///
  /// Variable region format state.
  ///
  UINT8   Format;
  ///
  /// Variable region healthy state.
  ///
  UINT8   State;
  UINT16  Reserved;
  UINT32  Reserved1;
} VARIABLE_STORE_HEADER;
"""
class VARIABLE_STORE_HEADER(ctypes.LittleEndianStructure):
    _fields_ = [
        ('Signature',                  guid_t),
        ('Size',                       uint32_t),
        ('Format',                     uint8_t),
        ('State',                      uint8_t),
        ('Reserved',                   uint16_t),
        ('Reserved1',                  uint32_t)
        ]
"""
///
/// Single Variable Data Header Structure.
///
typedef struct {
  ///
  /// Variable Data Start Flag.
  ///
  UINT16      StartId;
  ///
  /// Variable State defined above.
  ///
  UINT8       State;
  UINT8       Reserved;
  ///
  /// Attributes of variable defined in UEFI specification.
  ///
  UINT32      Attributes;
  ///
  /// Size of variable null-terminated Unicode string name.
  ///
  UINT32      NameSize;
  ///
  /// Size of the variable data without this header.
  ///
  UINT32      DataSize;
  ///
  /// A unique identifier for the vendor that produces and consumes this varaible.
  ///
  EFI_GUID    VendorGuid;
} VARIABLE_HEADER;
"""
class VARIABLE_HEADER(ctypes.LittleEndianStructure):
    _fields_ = [
        ('StartId',                     uint16_t),
        ('State',                       uint8_t),
        ('Reserved',                    uint8_t),
        ('Attributes',                  uint32_t),
        ('NameSize',                    uint32_t),
        ('DataSize',                    uint32_t),
        ('VendorGuid',                  guid_t)
        ]
"""
///
/// Single Variable Data Header Structure.
///
typedef struct {
  ///
  /// Variable Data Start Flag.
  ///
  UINT16      StartId;
  ///
  /// Variable State defined above.
  ///
  UINT8       State;
  UINT8       Reserved;
  ///
  /// Attributes of variable defined in UEFI specification.
  ///
  UINT32      Attributes;
  ///
  /// Associated monotonic count value against replay attack.
  ///
  UINT64      MonotonicCount;
  ///
  /// Associated TimeStamp value against replay attack. 
  ///
  EFI_TIME    TimeStamp;
  ///
  /// Index of associated public key in database.
  ///
  UINT32      PubKeyIndex;
  ///
  /// Size of variable null-terminated Unicode string name.
  ///
  UINT32      NameSize;
  ///
  /// Size of the variable data without this header.
  ///
  UINT32      DataSize;
  ///
  /// A unique identifier for the vendor that produces and consumes this varaible.
  ///
  EFI_GUID    VendorGuid;
} VARIABLE_HEADER;
"""
class AUTH_VARIABLE_HEADER(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('StartId',                     uint16_t),
        ('State',                       uint8_t),
        ('Reserved',                    uint8_t),
        ('Attributes',                  uint32_t),
        ('MonotonicCount',              uint64_t),
        ('TimeStamp',                   efi_time),
        ('PubKeyIndex',                 uint32_t),
        ('NameSize',                    uint32_t),
        ('DataSize',                    uint32_t),
        ('VendorGuid',                  guid_t)
        ]