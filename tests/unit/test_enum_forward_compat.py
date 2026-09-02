"""Package-wide invariant: API-sourced enums must tolerate unknown values.

This generalizes two point fixes. Issue #78 (an unrecognized ``SocketCategory``)
and the unrecognized ``generic`` purl type were the same bug: the Socket
API added an enum value, the SDK coerced it strictly inside ``from_dict``, and
the resulting ``ValueError`` emptied an entire response instead of degrading one
field. Each was fixed on the one enum that happened to fire, leaving the others
holding the same landmine.

Rather than add a third bespoke regression test the next time it happens, this
discovers every ``Enum`` in the package -- including ones added after this file
was written -- and asserts the invariant directly. A new enum has to opt out
explicitly and say why.
"""

import enum
import importlib
import logging
import pkgutil
import unittest

import socketdev

# Enums that are only ever used to *build* requests, never to parse a response.
# Strictness is correct there: a bad value is the caller's typo and should raise
# rather than be silently coerced. Add an entry only with a comment justifying
# that the enum never sees API-supplied values.
REQUEST_ONLY_ENUMS = frozenset()

# A value the API will never legitimately send.
SENTINEL = "__value_the_api_would_never_send__"


def _all_enums():
    """Every Enum subclass defined under the socketdev package."""
    found = {}
    for module_info in pkgutil.walk_packages(
        socketdev.__path__, prefix="socketdev."
    ):
        try:
            module = importlib.import_module(module_info.name)
        except Exception:  # pragma: no cover - an unimportable module is its own bug
            continue
        for name in dir(module):
            obj = getattr(module, name)
            if (
                isinstance(obj, type)
                and issubclass(obj, enum.Enum)
                and obj.__module__.startswith("socketdev")
                and len(obj) > 0
            ):
                found[f"{obj.__module__}.{obj.__name__}"] = obj
    return found


class TestEnumForwardCompatibility(unittest.TestCase):
    """Every response-parsed enum degrades instead of raising."""

    def test_enums_are_discovered(self):
        # Guards against the discovery walk silently finding nothing, which
        # would make every other test in this file vacuously pass.
        self.assertGreaterEqual(
            len(_all_enums()), 6, "enum discovery found suspiciously few enums"
        )

    def test_unknown_value_does_not_raise(self):
        for qualname, enum_cls in sorted(_all_enums().items()):
            if enum_cls.__name__ in REQUEST_ONLY_ENUMS:
                continue
            with self.subTest(enum=qualname):
                try:
                    result = enum_cls(SENTINEL)
                except ValueError:
                    self.fail(
                        f"{qualname} raised ValueError on an unrecognized value. "
                        f"Add a _missing_ that returns a documented fallback "
                        f"(see socketdev/core/enums.py), or add it to "
                        f"REQUEST_ONLY_ENUMS with a justification."
                    )
                self.assertIsInstance(
                    result,
                    enum_cls,
                    f"{qualname}._missing_ must return a member of its own enum",
                )

    def test_unknown_value_warns(self):
        # The fallback is a silent downgrade in accuracy, so it has to leave a
        # trace that something drifted.
        for qualname, enum_cls in sorted(_all_enums().items()):
            if enum_cls.__name__ in REQUEST_ONLY_ENUMS:
                continue
            with self.subTest(enum=qualname):
                with self.assertLogs("socketdev", level=logging.WARNING) as captured:
                    enum_cls(SENTINEL)
                self.assertTrue(
                    any(enum_cls.__name__ in line for line in captured.output),
                    f"{qualname} fell back without naming itself in the warning; "
                    f"got: {captured.output}",
                )

    def test_known_values_still_round_trip(self):
        # Forward-compat must not swallow legitimate values.
        for qualname, enum_cls in sorted(_all_enums().items()):
            for member in enum_cls:
                with self.subTest(enum=qualname, member=member.name):
                    self.assertIs(enum_cls(member.value), member)


if __name__ == "__main__":
    unittest.main()
