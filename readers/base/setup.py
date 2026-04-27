# This file is derived from https://github.com/pktrigg/pygsf , licensed under the Apache License, Version 2.0.
# Modified by Spatialnetics Inc. in 2026.

"""Setup script for pygsf package."""

from setuptools import setup, find_packages

setup(
    name="pygsf",
    version="0.1.0",
    description="Python library for reading and writing Generic Sensor Format (GSF) files",
    author="Guardian Geomatics",
    author_email="p.kennedy@guardiangeomatics.com",
    license="See LICENSE file",
    packages=find_packages(),
    py_modules=['pygsf'],
    install_requires=[
        'numpy>=1.20.0',
    ],
    python_requires=">=3.7",
)

