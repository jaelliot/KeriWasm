# -*- encoding: utf-8 -*-
"""
hio.help package - Minimal version for Pyodide
Console-only logging (no filesystem/syslog in browser)
"""

from . import ogling

# Module-level ogler singleton (console-only in Pyodide)
ogler = ogling.initOgler(prefix='hio')

from .helping import isNonStringIterable, isNonStringSequence, isIterator, Reat
from .decking import Deck
from .hicting import Hict, Mict
from .timing import (Timer, MonoTimer, TimerError, RetroTimerError,
                     nowIso8601, toIso8601, fromIso8601)
