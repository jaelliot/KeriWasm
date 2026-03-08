# -*- encoding: utf-8 -*-
"""
hio package - Pyodide-compatible subset for browser environments
Excludes TCP/UDP networking, serial, and lmdb-based modules
"""

__version__ = '0.7.19-pyodide'

from .hioing import (Mixin, HioError, SizeError, ValidationError, VersionError,
                     OglerError, FilerError, NamerError, HierError)
