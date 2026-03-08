"""
test_dep_chain.py — Dependency chain import test for keripy in Pyodide.

Systematically attempts to import every dependency that keripy requires,
reports which succeed and which fail. Designed to run inside Pyodide via
pyscript or the hio TestRunnerDoer.

Usage (standalone in Pyodide):
    import test_dep_chain
    results = test_dep_chain.run_all()
    # results is a dict of {module_name: True/str_error}

Usage (via TestRunnerDoer):
    from test_dep_chain import load_dep_chain_tests
    test_queue = load_dep_chain_tests()
"""

import sys
import importlib
from typing import List, Tuple, Any, Callable, Optional

TestEntry = Tuple[str, Optional[Callable[..., Any]], Tuple[Any, ...]]


# --- Individual import test functions ---

def _try_import(module_path: str) -> None:
    """Attempt to import a module; raises on failure."""
    importlib.import_module(module_path)


def test_import_msgpack():
    """Test msgpack (binary serialization)."""
    import msgpack
    packed = msgpack.packb({"test": True})
    assert isinstance(packed, bytes), "packb should return bytes"
    unpacked = msgpack.unpackb(packed)
    assert unpacked == {"test": True}, f"roundtrip failed: {unpacked}"


def test_import_cbor2():
    """Test cbor2 (CBOR serialization)."""
    import cbor2
    encoded = cbor2.dumps({"hello": "world"})
    assert isinstance(encoded, bytes)
    decoded = cbor2.loads(encoded)
    assert decoded == {"hello": "world"}


def test_import_multidict():
    """Test multidict (multi-value dict for HTTP headers)."""
    from multidict import CIMultiDict
    d = CIMultiDict([("Content-Type", "text/plain")])
    assert d["content-type"] == "text/plain"


def test_import_jsonschema():
    """Test jsonschema (JSON validation)."""
    import jsonschema
    schema = {"type": "object", "properties": {"name": {"type": "string"}}}
    jsonschema.validate({"name": "test"}, schema)


def test_import_ordered_set():
    """Test ordered-set."""
    from ordered_set import OrderedSet
    s = OrderedSet([3, 1, 2, 1])
    assert list(s) == [3, 1, 2]


def test_import_pyyaml():
    """Test PyYAML."""
    import yaml
    data = yaml.safe_load("key: value")
    assert data == {"key": "value"}


def test_import_hjson():
    """Test hjson (human JSON)."""
    import hjson
    data = hjson.loads('{ key: value }')
    assert data == {"key": "value"}


def test_import_http_sfv():
    """Test http-sfv (structured field values)."""
    import http_sfv
    assert hasattr(http_sfv, "Dictionary") or hasattr(http_sfv, "Item")


def test_import_semver():
    """Test semver."""
    import semver
    v = semver.Version.parse("1.2.3")
    assert v.major == 1


def test_import_blake3():
    """Test blake3 (WASM wheel)."""
    import blake3
    h = blake3.blake3(b"hello").hexdigest()
    assert len(h) == 64


def test_import_cryptography():
    """Test cryptography (Ed25519)."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    key = Ed25519PrivateKey.generate()
    assert key is not None


def test_import_pysodium():
    """Test pysodium shim (→ pychloride)."""
    import pysodium
    # Basic function availability
    assert hasattr(pysodium, "crypto_sign_keypair") or hasattr(pysodium, "crypto_generichash")


def test_import_lmdb_shim():
    """Test lmdb shim (should exist but raise NotImplementedError on use)."""
    import lmdb
    # The shim should be importable
    assert lmdb is not None


def test_import_mnemonic():
    """Test mnemonic (BIP39 word lists)."""
    import mnemonic
    m = mnemonic.Mnemonic("english")
    assert m is not None


# --- hio module import tests ---

def test_import_hio():
    """Test hio package root."""
    import hio
    assert hio.__version__.startswith("0.7")
    assert hasattr(hio, "HioError")


def test_import_hio_hioing():
    """Test hio.hioing exceptions."""
    from hio.hioing import (HioError, SizeError, ValidationError,
                            VersionError, OglerError, HierError)


def test_import_hio_base_doing():
    """Test hio.base.doing (scheduler)."""
    from hio.base import doing
    assert hasattr(doing, "Doist")
    assert hasattr(doing, "Doer")
    assert hasattr(doing, "doize")


def test_import_hio_base_tyming():
    """Test hio.base.tyming (time management)."""
    from hio.base import tyming
    assert hasattr(tyming, "Tymist")
    assert hasattr(tyming, "Tymer")


def test_import_hio_help_decking():
    """Test hio.help.decking (Deck class)."""
    from hio.help import decking
    d = decking.Deck()
    d.push("item")
    assert d.pull() == "item"
    assert d.pull(emptive=True) is None


def test_import_hio_help_ogling():
    """Test hio.help.ogling (logging)."""
    from hio.help import ogling
    ogler = ogling.initOgler(prefix='test')
    logger = ogler.getLogger('test_dep_chain')
    assert logger is not None


def test_import_hio_help_ogler():
    """Test hio.help.ogler (module-level singleton)."""
    from hio.help import ogler
    assert ogler is not None
    logger = ogler.getLogger('test_dep_chain')
    assert logger is not None


def test_import_hio_help_hicting():
    """Test hio.help.hicting (case-insensitive dict)."""
    from hio.help import Hict, Mict
    h = Hict([("Content-Type", "text/plain")])
    assert h["content-type"] == "text/plain"


def test_import_hio_help_timing():
    """Test hio.help.timing (timers + ISO 8601)."""
    from hio.help.timing import Timer, MonoTimer, nowIso8601
    ts = nowIso8601()
    assert "T" in ts  # ISO 8601 format


def test_import_hio_help_helping():
    """Test hio.help.helping (utilities)."""
    from hio.help.helping import isNonStringIterable, isNonStringSequence, Reat
    assert isNonStringIterable([1, 2, 3])
    assert not isNonStringIterable("hello")
    assert Reat.match("valid_name")


def test_import_hio_core_http():
    """Test hio.core.http.httping (HTTP parsing)."""
    from hio.core.http import httping
    assert hasattr(httping, "Parsent")
    assert hasattr(httping, "normalizeHostPort")


def test_import_hio_bridge():
    """Test hio_bridge (WebDoist)."""
    try:
        from hio_bridge import WebDoist, AsyncRecurDoer
    except ImportError:
        # May not be on sys.path in all test configurations
        _try_import("hio_bridge")


# --- Aggregate test loading ---

ALL_DEP_TESTS = [
    # Section: Pure Python packages
    ("=== PURE PYTHON PACKAGES ===", None, ()),
    ("msgpack", test_import_msgpack, ()),
    ("cbor2", test_import_cbor2, ()),
    ("multidict", test_import_multidict, ()),
    ("jsonschema", test_import_jsonschema, ()),
    ("ordered_set", test_import_ordered_set, ()),
    ("pyyaml", test_import_pyyaml, ()),
    ("hjson", test_import_hjson, ()),
    ("http_sfv", test_import_http_sfv, ()),
    ("semver", test_import_semver, ()),
    ("mnemonic", test_import_mnemonic, ()),

    # Section: WASM/native wheels
    ("=== WASM COMPILED PACKAGES ===", None, ()),
    ("blake3", test_import_blake3, ()),
    ("cryptography", test_import_cryptography, ()),

    # Section: Shims
    ("=== SHIMS (pysodium, lmdb) ===", None, ()),
    ("pysodium_shim", test_import_pysodium, ()),
    ("lmdb_shim", test_import_lmdb_shim, ()),

    # Section: hio modules
    ("=== HIO PACKAGE ===", None, ()),
    ("hio", test_import_hio, ()),
    ("hio.hioing", test_import_hio_hioing, ()),
    ("hio.base.doing", test_import_hio_base_doing, ()),
    ("hio.base.tyming", test_import_hio_base_tyming, ()),
    ("hio.help.decking", test_import_hio_help_decking, ()),
    ("hio.help.ogling", test_import_hio_help_ogling, ()),
    ("hio.help.ogler", test_import_hio_help_ogler, ()),
    ("hio.help.hicting", test_import_hio_help_hicting, ()),
    ("hio.help.timing", test_import_hio_help_timing, ()),
    ("hio.help.helping", test_import_hio_help_helping, ()),
    ("hio.core.http", test_import_hio_core_http, ()),
]


def load_dep_chain_tests() -> List[TestEntry]:
    """Return test queue entries for TestRunnerDoer."""
    return list(ALL_DEP_TESTS)


def run_all() -> dict:
    """Run all tests directly, return dict of results.

    Returns:
        dict mapping test name to True (pass) or error string (fail).
    """
    results = {}
    for name, func, args in ALL_DEP_TESTS:
        if func is None:
            continue  # section header
        try:
            func(*args)
            results[name] = True
        except Exception as e:
            results[name] = f"{type(e).__name__}: {e}"
    return results
