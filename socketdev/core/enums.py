"""Forward-compatibility helpers for enums sourced from the Socket API.

The Socket API adds values to its enums (purl types, alert categories, policy
actions) without a corresponding SDK release. When a strict ``Enum`` coercion
meets one of those values it raises ``ValueError``, and because coercion happens
inside ``from_dict`` that error takes down the whole response parse rather than
the single field it applies to. That is how issue #78 (an unknown
``SocketCategory``) and the unknown ``generic`` purl type each produced
empty reports from otherwise-successful scans.

Every enum in this package that is populated from an API response therefore
defines ``_missing_`` and falls back to a documented sentinel instead of
raising. ``tests/unit/test_enum_forward_compat.py`` enforces that as an
invariant across the package, including for enums added later.
"""

import logging

log = logging.getLogger("socketdev")


def unknown_enum_value(enum_name: str, value: object, fallback):
    """Log an unrecognized API enum value and return the enum's fallback member.

    Callers are ``_missing_`` implementations, so returning ``fallback`` is what
    turns the would-be ``ValueError`` into a usable member.
    """
    log.warning(
        "Unknown %s %r; falling back to %s. "
        "Upgrade socketdev to pick up newer values.",
        enum_name,
        value,
        fallback.name,
    )
    return fallback
