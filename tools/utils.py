"""
Shared utility functions for GSF file processing.
"""
import struct
from datetime import datetime
from typing import List, Tuple, Union

import numpy as np


def posix_seconds(value: Union[str, np.datetime64, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Convert a time decoded by gsfu to POSIX seconds.

    gsfu returns a ping's PingTime as an ISO 8601 string with a UTC offset,
    and attitude measurement times as a numpy datetime64 array. The tools
    report times as POSIX seconds, so this converts either form.

    Args:
        value: An ISO 8601 string, a numpy datetime64 value, or a numpy
            datetime64 array.

    Returns:
        The time in POSIX seconds, as a float for a single value or as a
        float64 array for an array.
    """
    if isinstance(value, str):
        return datetime.fromisoformat(value).timestamp()
    nanoseconds = np.asarray(value).astype("datetime64[ns]").astype(np.int64)
    seconds = nanoseconds / 1e9
    return float(seconds) if seconds.ndim == 0 else seconds


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

