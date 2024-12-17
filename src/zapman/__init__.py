"""Zapman.

A Python tool for API testing and development in your terminal.
"""

from zapman._context import After, Test
from zapman._store import ContextStore, CookieStoreWrapper
from zapman._version import __version__

env = ContextStore()
cookies = CookieStoreWrapper()

# A small public API, as small as possible
__all__ = ["After", "Test", "__version__", "cookies", "env"]
