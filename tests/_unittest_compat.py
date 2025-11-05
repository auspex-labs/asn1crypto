# coding: utf-8

"""
Unittest compatibility shim - no-op for Python 3.9+

This module previously provided Python 2.6/2.7 compatibility shims
for unittest. Since asn1crypto now requires Python 3.9+, this is
maintained only for backward compatibility with test imports.
"""


def patch():
    """
    No-op function for Python 3.9+ - all unittest features are built-in
    """
    pass
