"""
Shared utility functions for GSF file processing.
"""
import struct
from typing import List, Tuple


def scan_subrecords(raw: bytes, ping_header_size: int) -> List[Tuple[int, bytes]]:
    """
    Scan subrecords from a raw datagram buffer.
    
    Given the raw datagram buffer (size+id(+checksum)+ping header+subrecords),
    return a list of (subrecord_id, payload_bytes) tuples.
    
    Args:
        raw: Raw datagram buffer bytes
        ping_header_size: Size of the ping header in bytes
        
    Returns:
        List of tuples containing (subrecord_id, payload_bytes)
    """
    _, ident = struct.unpack(">II", raw[:8])
    has_checksum = ((ident >> 31) & 1) == 1
    offset = 8 + (4 if has_checksum else 0) + ping_header_size
    total = len(raw)
    subs = []
    while offset + 4 <= total:
        sub_id = raw[offset]
        length = int.from_bytes(raw[offset+1:offset+4], "big")
        payload = raw[offset+4:offset+4+length]
        subs.append((sub_id, payload))
        offset += 4 + length
    return subs


def scan_subrecord_ids(raw: bytes, ping_header_size: int) -> List[int]:
    """
    Scan subrecord IDs from a raw datagram buffer.
    
    Given the raw datagram buffer (size+id(+checksum)+ping header+subrecords),
    return a list of subrecord IDs only.
    
    Args:
        raw: Raw datagram buffer bytes
        ping_header_size: Size of the ping header in bytes
        
    Returns:
        List of subrecord IDs
    """
    _, ident = struct.unpack(">II", raw[:8])
    has_checksum = ((ident >> 31) & 1) == 1
    offset = 8 + (4 if has_checksum else 0) + ping_header_size
    subs = []
    total = len(raw)
    while offset + 4 <= total:
        sub_id = raw[offset]
        length = int.from_bytes(raw[offset+1:offset+4], "big")
        subs.append(sub_id)
        offset += 4 + length
    return subs

