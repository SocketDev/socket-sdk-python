"""
Unit tests for lenient SocketPURL_Type parsing (CE-362).

The Socket API can emit purl types the SDK does not yet know about (e.g.
``"generic"``, which was missing from the enum entirely). Strict enum parsing
turned one such artifact into a hard failure for the whole full-scan stream:
``FullScanStreamResponse.from_dict`` raised, ``FullScans.stream`` returned
``success=False`` with no artifacts, and consumers (notably socketsecurity)
produced empty reports for otherwise-successful scans.

These tests pin two behaviors:

1. ``SocketPURL_Type`` resolves known purl types (including ``generic``) and
   falls back to ``UNKNOWN`` with a warning for unrecognized values, mirroring
   the ``SocketCategory`` forward-compat approach from issue #78.
2. ``FullScanStreamResponse.from_dict`` skips individual artifacts that fail to
   parse instead of discarding the entire response.
"""

import json
import logging
import unittest

from socketdev.fullscans import (
    FullScans,
    FullScanStreamResponse,
    SocketArtifact,
    SocketPURL,
    SocketPURL_Type,
)


def _artifact_payload(artifact_id: str, purl_type: str) -> dict:
    return {
        "id": artifact_id,
        "type": purl_type,
        "name": "example-package",
        "version": "1.0.0",
        "alerts": [],
    }


class TestSocketPURLTypeParsing(unittest.TestCase):
    """SocketPURL_Type should tolerate unknown purl type values."""

    def test_generic_is_recognized(self):
        self.assertEqual(SocketPURL_Type("generic"), SocketPURL_Type.GENERIC)

    def test_common_ecosystems_are_recognized(self):
        for value in ("npm", "pypi", "golang", "maven", "gem", "nuget", "cargo"):
            self.assertEqual(SocketPURL_Type(value).value, value)

    def test_unknown_type_falls_back_to_unknown(self):
        self.assertEqual(
            SocketPURL_Type("someFutureEcosystem"), SocketPURL_Type.UNKNOWN
        )

    def test_unknown_type_emits_warning(self):
        with self.assertLogs("socketdev", level=logging.WARNING) as captured:
            SocketPURL_Type("someFutureEcosystem")
        self.assertTrue(
            any("Unknown SocketPURL_Type" in message for message in captured.output),
            f"expected a warning about the unknown purl type, got: {captured.output}",
        )

    def test_socket_purl_from_dict_does_not_raise(self):
        purl = SocketPURL.from_dict({"type": "someFutureEcosystem", "name": "pkg"})
        self.assertEqual(purl.type, SocketPURL_Type.UNKNOWN)

    def test_socket_artifact_from_dict_with_generic_type(self):
        artifact = SocketArtifact.from_dict(_artifact_payload("a1", "generic"))
        self.assertEqual(artifact.type, SocketPURL_Type.GENERIC)
        self.assertEqual(artifact.name, "example-package")


class TestFullScanStreamResponseResilience(unittest.TestCase):
    """One bad artifact should not empty out the whole stream response."""

    def test_generic_artifact_is_kept(self):
        response = FullScanStreamResponse.from_dict(
            {
                "success": True,
                "status": 200,
                "artifacts": {
                    "a1": _artifact_payload("a1", "npm"),
                    "a2": _artifact_payload("a2", "generic"),
                },
            }
        )
        self.assertEqual(set(response.artifacts), {"a1", "a2"})
        self.assertEqual(response.artifacts["a2"].type, SocketPURL_Type.GENERIC)

    def test_malformed_artifact_is_skipped_not_fatal(self):
        payload = {
            "success": True,
            "status": 200,
            "artifacts": {
                "good": _artifact_payload("good", "npm"),
                # Missing required "id" field, so SocketArtifact.from_dict raises.
                "bad": {"type": "npm", "alerts": []},
            },
        }
        with self.assertLogs("socketdev", level=logging.WARNING) as captured:
            response = FullScanStreamResponse.from_dict(payload)
        self.assertEqual(list(response.artifacts), ["good"])
        self.assertTrue(
            any("Skipping artifact bad" in message for message in captured.output),
            f"expected a warning about the skipped artifact, got: {captured.output}",
        )

    def test_full_scans_stream_skips_artifact_without_id(self):
        class Response:
            status_code = 200
            text = "\n".join(
                json.dumps(artifact)
                for artifact in (
                    _artifact_payload("good", "npm"),
                    {"type": "npm", "name": "bad", "alerts": []},
                )
            )

        class API:
            def do_request(self, **kwargs):
                return Response()

        with self.assertLogs("socketdev", level=logging.WARNING) as captured:
            response = FullScans(API()).stream("org", "scan", use_types=True)

        self.assertTrue(response.success)
        self.assertEqual(list(response.artifacts), ["good"])
        self.assertTrue(
            any(
                "Skipping artifact without a usable id" in message
                for message in captured.output
            ),
            f"expected a warning about the skipped artifact, got: {captured.output}",
        )


if __name__ == "__main__":
    unittest.main()
