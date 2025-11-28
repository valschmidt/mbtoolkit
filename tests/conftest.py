"""
Pytest configuration and shared fixtures.
"""
import pytest
import tempfile
import os


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_profile():
    """Create a sample profile JSON for testing."""
    return {
        "profile": {
            "name": "Test Profile",
            "gsf_version": "03.11",
            "description": "A test profile for unit testing",
            "coordinate_reference": {
                "horizontal_datum": "WGS-84",
                "vertical_datum": "WGS-84 geoid"
            },
            "required_records": [
                {
                    "record_type": "HeaderRecord",
                    "record_id": 1,
                    "description": "GSF file format version tag"
                },
                {
                    "record_type": "SwathBathymetryPing",
                    "record_id": 2,
                    "required_header_fields": [
                        "timestamp",
                        "latitude",
                        "longitude"
                    ],
                    "required_subrecords": [
                        {
                            "subrecord_name": "ScaleFactors",
                            "subrecord_id": 100
                        },
                        {
                            "subrecord_name": "DepthArray",
                            "subrecord_id": 1
                        }
                    ]
                }
            ]
        }
    }

