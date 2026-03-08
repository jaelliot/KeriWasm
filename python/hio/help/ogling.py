# -*- encoding: utf-8 -*-
"""hio.help.ogling module — Pyodide-safe version

Console-only logging for browser environments.
Filesystem and syslog handlers are disabled (no /dev/log, no temp dirs).
"""
import sys
import logging
from contextlib import contextmanager

from ..hioing import OglerError


def initOgler(level=logging.CRITICAL, **kwa):
    """Initialize module-level Ogler singleton (console-only for Pyodide)."""
    return Ogler(level=level, **kwa)


@contextmanager
def openOgler(cls=None, name="test", temp=True, **kwa):
    """Context manager for Ogler instances."""
    ogler = None
    if cls is None:
        cls = Ogler
    try:
        ogler = cls(name=name, temp=temp, reopen=True, **kwa)
        yield ogler
    finally:
        if ogler:
            ogler.close()


class Ogler:
    """Console-only Ogler for Pyodide/browser environments.

    Preserves the same public API as the real hio Ogler but only outputs
    to stderr (console) since the browser has no filesystem or syslog.

    Attributes match upstream hio Ogler for compatibility.
    """
    Prefix = "hio"

    def __init__(self, name='main', level=logging.ERROR, temp=False,
                 prefix=None, headDirPath=None, reopen=False, clear=False,
                 consoled=True, syslogged=False, filed=False,
                 when='H', interval=1, count=48):
        self.name = name if name else 'main'
        self.level = level
        self.temp = True if temp else False
        self.prefix = prefix if prefix is not None else self.Prefix
        self.headDirPath = headDirPath
        self.dirPath = None
        self.path = None
        self.opened = False
        self.consoled = True  # always console in browser
        self.syslogged = False  # no syslog in browser
        self.filed = False  # no filesystem logging in browser

        fmt = "{}: %(message)s".format(self.prefix)
        self.baseFormatter = logging.Formatter(fmt)
        self.baseConsoleHandler = logging.StreamHandler()
        self.baseConsoleHandler.setFormatter(self.baseFormatter)

        if reopen:
            self.reopen(headDirPath=self.headDirPath, clear=clear)

    def reopen(self, name=None, temp=None, headDirPath=None, clear=False):
        """No-op for filesystem; console handler is always active."""
        if name is not None:
            self.name = name
        self.opened = True

    def close(self, clear=False):
        """Mark as closed."""
        self.opened = False

    def clearDirPath(self):
        """No-op in browser."""

    def resetLevel(self, name=__name__, level=None, globally=False):
        """Reset logging level of named logger."""
        level = level if level is not None else self.level
        if globally:
            self.level = level
        logger = logging.getLogger(name)
        logger.setLevel(level)

    def getLogger(self, name=__name__, level=None):
        """Return a stdlib logger with console handler attached."""
        logger = logging.getLogger(name)
        logger.propagate = False
        level = level if level is not None else self.level
        logger.setLevel(level)
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
        logger.addHandler(self.baseConsoleHandler)
        return logger
