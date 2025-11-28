"""
Tests for utility functions.
"""
import pytest
import struct
from tools.utils import scan_subrecords, scan_subrecord_ids


class TestScanSubrecords:
    """Tests for scan_subrecords function."""

    def test_scan_subrecords_basic(self):
        """Test scanning subrecords with basic structure."""
        # Create a mock datagram: size(4) + id(4) + ping_header(60) + subrecords
        ping_header_size = 60
        ping_header = b'\x00' * ping_header_size
        
        # Subrecord 1: ID=1, length=4, payload=4 bytes
        subrecord1 = struct.pack(">B", 1) + struct.pack(">I", 4)[1:] + b"data"
        # Subrecord 2: ID=2, length=3, payload=3 bytes
        subrecord2 = struct.pack(">B", 2) + struct.pack(">I", 3)[1:] + b"xyz"
        
        # Build datagram: size + id (no checksum) + header + subrecords
        datagram_size = 4 + 4 + ping_header_size + len(subrecord1) + len(subrecord2)
        size_word = struct.pack(">I", datagram_size - 4)  # size excludes size word itself
        id_word = struct.pack(">I", 0x00000002)  # Record ID 2, no checksum bit
        
        raw = size_word + id_word + ping_header + subrecord1 + subrecord2
        
        result = scan_subrecords(raw, ping_header_size)
        
        assert len(result) == 2
        assert result[0] == (1, b"data")
        assert result[1] == (2, b"xyz")

    def test_scan_subrecords_empty(self):
        """Test scanning subrecords when there are none."""
        ping_header_size = 60
        ping_header = b'\x00' * ping_header_size
        
        datagram_size = 4 + 4 + ping_header_size
        size_word = struct.pack(">I", datagram_size - 4)
        id_word = struct.pack(">I", 0x00000002)
        
        raw = size_word + id_word + ping_header
        
        result = scan_subrecords(raw, ping_header_size)
        
        assert len(result) == 0
        assert result == []

    def test_scan_subrecords_with_checksum(self):
        """Test scanning subrecords when checksum is present."""
        ping_header_size = 60
        ping_header = b'\x00' * ping_header_size
        
        # Subrecord: ID=100, length=2, payload=2 bytes
        subrecord = struct.pack(">B", 100) + struct.pack(">I", 2)[1:] + b"ab"
        
        # Build datagram with checksum (bit 31 set in id word)
        datagram_size = 4 + 4 + 4 + ping_header_size + len(subrecord)  # +4 for checksum
        size_word = struct.pack(">I", datagram_size - 4)
        id_word = struct.pack(">I", 0x80000002)  # Checksum bit set
        checksum = struct.pack(">I", 0x12345678)
        
        raw = size_word + id_word + checksum + ping_header + subrecord
        
        result = scan_subrecords(raw, ping_header_size)
        
        assert len(result) == 1
        assert result[0] == (100, b"ab")


class TestScanSubrecordIds:
    """Tests for scan_subrecord_ids function."""

    def test_scan_subrecord_ids_basic(self):
        """Test scanning subrecord IDs with basic structure."""
        ping_header_size = 60
        ping_header = b'\x00' * ping_header_size
        
        subrecord1 = struct.pack(">B", 1) + struct.pack(">I", 4)[1:] + b"data"
        subrecord2 = struct.pack(">B", 2) + struct.pack(">I", 3)[1:] + b"xyz"
        
        datagram_size = 4 + 4 + ping_header_size + len(subrecord1) + len(subrecord2)
        size_word = struct.pack(">I", datagram_size - 4)
        id_word = struct.pack(">I", 0x00000002)
        
        raw = size_word + id_word + ping_header + subrecord1 + subrecord2
        
        result = scan_subrecord_ids(raw, ping_header_size)
        
        assert len(result) == 2
        assert result == [1, 2]

    def test_scan_subrecord_ids_empty(self):
        """Test scanning subrecord IDs when there are none."""
        ping_header_size = 60
        ping_header = b'\x00' * ping_header_size
        
        datagram_size = 4 + 4 + ping_header_size
        size_word = struct.pack(">I", datagram_size - 4)
        id_word = struct.pack(">I", 0x00000002)
        
        raw = size_word + id_word + ping_header
        
        result = scan_subrecord_ids(raw, ping_header_size)
        
        assert len(result) == 0
        assert result == []

    def test_scan_subrecord_ids_multiple(self):
        """Test scanning multiple subrecord IDs."""
        ping_header_size = 60
        ping_header = b'\x00' * ping_header_size
        
        subrecords = []
        for i in range(5):
            payload = b"x" * i
            subrecord = struct.pack(">B", i + 10) + struct.pack(">I", len(payload))[1:] + payload
            subrecords.append(subrecord)
        
        total_subrecord_size = sum(len(s) for s in subrecords)
        datagram_size = 4 + 4 + ping_header_size + total_subrecord_size
        size_word = struct.pack(">I", datagram_size - 4)
        id_word = struct.pack(">I", 0x00000002)
        
        raw = size_word + id_word + ping_header + b"".join(subrecords)
        
        result = scan_subrecord_ids(raw, ping_header_size)
        
        assert len(result) == 5
        assert result == [10, 11, 12, 13, 14]

