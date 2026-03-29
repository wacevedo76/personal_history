#!/usr/bin/env python3
"""
Setup script for Personal History (root level)
Install from this directory: pip install -e .
"""

from setuptools import setup, find_packages

setup(
    name="personal-history",
    version="0.01.0",
    description="Personal History Format Implementation",
    author="William Acevedo",
    packages=find_packages(),
    install_requires=[
        "cryptography>=42.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ph=personal_history.ph.v001.cli:main",
        ],
    },
    python_requires=">=3.8",
)