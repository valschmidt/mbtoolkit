# This file is derived from https://github.com/pktrigg/pygsf , licensed under the Apache License, Version 2.0.
# Modified by Spatialnetics Inc. in 2026.

"""
pygsf - Python library for reading and writing Generic Sensor Format (GSF) files.

This module provides classes and constants for working with GSF files.
"""

# Import everything from the pygsf.py module file
# We need to import from the .py file to avoid circular imports
import importlib.util
import os

# Get the directory containing this __init__.py
_package_dir = os.path.dirname(os.path.abspath(__file__))
_pygsf_module_path = os.path.join(_package_dir, 'pygsf.py')

if not os.path.exists(_pygsf_module_path):
    raise ImportError(f"pygsf.py not found at {_pygsf_module_path}")

# Load the pygsf.py module
spec = importlib.util.spec_from_file_location("pygsf._pygsf", _pygsf_module_path)
if spec is None or spec.loader is None:
    raise ImportError("Could not create spec for pygsf.py module")

_pygsf_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_pygsf_module)

# Export the key classes and constants
GSFREADER = _pygsf_module.GSFREADER
SWATH_BATHYMETRY = _pygsf_module.SWATH_BATHYMETRY
ATTITUDE = _pygsf_module.ATTITUDE
HEADER = _pygsf_module.HEADER
SOUND_VELOCITY_PROFILE = _pygsf_module.SOUND_VELOCITY_PROFILE
PROCESSING_PARAMETERS = _pygsf_module.PROCESSING_PARAMETERS
SENSOR_PARAMETERS = _pygsf_module.SENSOR_PARAMETERS
COMMENT = _pygsf_module.COMMENT
HISTORY = _pygsf_module.HISTORY
NAVIGATION_ERROR = _pygsf_module.NAVIGATION_ERROR
SWATH_BATHY_SUMMARY = _pygsf_module.SWATH_BATHY_SUMMARY
SINGLE_BEAM_SOUNDING = _pygsf_module.SINGLE_BEAM_SOUNDING
HV_NAVIGATION_ERROR = _pygsf_module.HV_NAVIGATION_ERROR
SNIPPET_NONE = _pygsf_module.SNIPPET_NONE
ARCIdx = _pygsf_module.ARCIdx

__all__ = [
    'GSFREADER',
    'SWATH_BATHYMETRY',
    'ATTITUDE',
    'HEADER',
    'SOUND_VELOCITY_PROFILE',
    'PROCESSING_PARAMETERS',
    'SENSOR_PARAMETERS',
    'COMMENT',
    'HISTORY',
    'NAVIGATION_ERROR',
    'SWATH_BATHY_SUMMARY',
    'SINGLE_BEAM_SOUNDING',
    'HV_NAVIGATION_ERROR',
    'SNIPPET_NONE',
    'ARCIdx',
]

