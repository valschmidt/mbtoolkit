"""
Tests for gsf-repair functionality.
"""
import pytest
import struct
import tempfile
import os
from tools.gsf_repair import make_empty_subrecord


class TestMakeEmptySubrecord:
    """Tests for make_empty_subrecord function."""

    def test_make_empty_subrecord_basic(self):
        """Test creating an empty subrecord."""
        sub_id = 1
        result = make_empty_subrecord(sub_id)
        
        # Should be 4 bytes: 1 byte ID + 3 bytes length (0)
        assert len(result) == 4
        assert result[0] == sub_id
        assert result[1:4] == b"\x00\x00\x00"

    def test_make_empty_subrecord_different_ids(self):
        """Test creating empty subrecords with different IDs."""
        for sub_id in [1, 100, 255]:
            result = make_empty_subrecord(sub_id)
            assert len(result) == 4
            assert result[0] == sub_id
            assert result[1:4] == b"\x00\x00\x00"

    def test_make_empty_subrecord_structure(self):
        """Test that empty subrecord has correct binary structure."""
        sub_id = 42
        result = make_empty_subrecord(sub_id)
        
        # Verify it can be unpacked correctly
        unpacked_id = result[0]
        unpacked_length = int.from_bytes(result[1:4], "big")
        
        assert unpacked_id == sub_id
        assert unpacked_length == 0

