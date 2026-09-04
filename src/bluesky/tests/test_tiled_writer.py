import sys
from importlib.metadata import PackageNotFoundError, version

import pytest
from packaging.version import Version

# bluesky_tiled_plugins gained the names imported by the deprecation shim
# modules in 2.0.10; older releases raise ImportError on import.
MIN_TILED_PLUGINS_VERSION = Version("2.0.10")

try:
    _tiled_plugins_version = Version(version("bluesky-tiled-plugins"))
except PackageNotFoundError:
    _tiled_plugins_version = None

tiled_plugins_too_old = pytest.mark.skipif(
    _tiled_plugins_version is None or _tiled_plugins_version < MIN_TILED_PLUGINS_VERSION,
    reason=f"requires bluesky-tiled-plugins >= {MIN_TILED_PLUGINS_VERSION}",
)


@tiled_plugins_too_old
def test_imports_raise_warnings():
    # Pop from `sys.modules` so the deprecation `warnings.warn(...)` at
    # the top of each shim module re-fires on (re)import.
    sys.modules.pop("bluesky.callbacks.tiled_writer", None)
    with pytest.warns(DeprecationWarning, match="bluesky.callbacks.tiled_writer"):
        import bluesky.callbacks.tiled_writer  # noqa: F401

    sys.modules.pop("bluesky.consolidators", None)
    with pytest.warns(DeprecationWarning, match="bluesky.consolidators"):
        import bluesky.consolidators  # noqa: F401
