#!/usr/bin/env python3
"""Compare this SDK's enums against the live Socket OpenAPI specification.

The SDK's enums are hand-maintained copies of value sets the API owns, and
nothing has ever told us when the API adds to one. Both prior incidents were
both found by a customer, after the fact, via an empty report.

The spec at ``https://api.socket.dev/v0/openapi`` is public and unauthenticated,
so this needs no token, no org and no fixture data -- it is a plain GET plus a
set comparison. It catches schema drift only; it deliberately says nothing about
runtime behaviour, response shapes or auth, which need the authenticated
integration checks.

Exit codes:
    0  no missing values (extras and unmapped enums are reported, not fatal)
    1  the API defines values this SDK does not know about
    2  the spec could not be fetched or parsed
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

from socketdev.fullscans import (
    DiffType,
    ScanType,
    SocketCategory,
    SocketIssueSeverity,
    SocketPURL_Type,
)
from socketdev.settings import SecurityAction

DEFAULT_SPEC_URL = "https://api.socket.dev/v0/openapi"

# SDK enum -> the schema in components/schemas that defines the same value set.
# None means the API does not expose the value set as a named schema, so this
# check cannot cover it; those are reported so the gap stays visible rather than
# looking like a pass.
ENUM_TO_SCHEMA = {
    SocketPURL_Type: "SocketPURL_Type",
    SocketIssueSeverity: "SocketIssueSeverity",
    SocketCategory: "SocketCategory",
    DiffType: "SocketDiffArtifactType",
    ScanType: None,
    SecurityAction: None,
}

# Members this SDK adds deliberately, which the API will never send. They are
# the documented _missing_ fallbacks (see socketdev/core/enums.py), so their
# absence from the spec is expected rather than drift.
SDK_ONLY_VALUES = {
    "SocketPURL_Type": {"unknown"},
    "SocketIssueSeverity": {"unknown"},
    "SocketCategory": {"miscellaneous"},
    "DiffType": {"unknown"},
}


def fetch_spec(url):
    with urllib.request.urlopen(url, timeout=60) as response:
        if response.status != 200:
            raise RuntimeError(f"{url} returned HTTP {response.status}")
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-url", default=DEFAULT_SPEC_URL)
    args = parser.parse_args()

    try:
        spec = fetch_spec(args.spec_url)
        schemas = spec["components"]["schemas"]
    except (urllib.error.URLError, KeyError, ValueError, RuntimeError) as exc:
        print(f"::error::could not read the OpenAPI spec: {exc}")
        return 2

    drifted = False
    unmapped = []

    for enum_cls, schema_name in ENUM_TO_SCHEMA.items():
        if schema_name is None:
            unmapped.append(enum_cls.__name__)
            continue
        schema = schemas.get(schema_name)
        if not schema or "enum" not in schema:
            print(
                f"::warning::schema {schema_name!r} for {enum_cls.__name__} is gone "
                f"or no longer an enum -- the API may have restructured it"
            )
            continue

        api_values = set(schema["enum"])
        sdk_values = {member.value for member in enum_cls}
        sdk_only = SDK_ONLY_VALUES.get(enum_cls.__name__, set())

        missing = sorted(api_values - sdk_values)
        extra = sorted(sdk_values - api_values - sdk_only)

        if missing:
            drifted = True
            print(
                f"::error::{enum_cls.__name__} is missing {len(missing)} value(s) "
                f"the API defines: {', '.join(missing)}"
            )
        if extra:
            # Not fatal: the spec omitting a value the SDK accepts is usually a
            # spec gap, and dropping a member would be a breaking change.
            print(
                f"::warning::{enum_cls.__name__} defines {len(extra)} value(s) "
                f"absent from the spec: {', '.join(extra)}"
            )
        if not missing and not extra:
            print(f"ok: {enum_cls.__name__} matches {schema_name} "
                  f"({len(api_values)} values)")

    if unmapped:
        print(
            f"::warning::not covered by this check, because the API exposes no "
            f"named schema for them: {', '.join(sorted(unmapped))}"
        )

    if drifted:
        print(
            "\nAdd the missing members to the SDK enum. Existing values are "
            "still parsed correctly in the meantime -- _missing_ maps unknown "
            "values to a fallback -- so this is a loss of fidelity, not an "
            "outage."
        )
        return 1

    print("\nno missing enum values")
    return 0


if __name__ == "__main__":
    sys.exit(main())
