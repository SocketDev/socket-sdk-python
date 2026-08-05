import json
import urllib.parse
import warnings
from typing import Optional
from socketdev.log import log
from socketdev.exceptions import APIPartialResponse
from ..core.dedupe import Dedupe


def _encode_bool_query_value(value) -> str:
    """Encode typed bools while preserving legacy string query values."""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


class Purl:
    def __init__(self, api):
        self.api = api

    def post(
        self,
        license: str = "false",
        components: list = None,
        org_slug: str = None,
        poll: Optional[bool] = None,
        timeout_sec: Optional[int] = None,
        alerts: Optional[bool] = None,
        purl_errors: Optional[bool] = None,
        strict: bool = False,
        **kwargs,
    ) -> list:
        """POST a batch of purls to the Socket batch purl endpoint and return deduped rows.

        The batch purl API (``POST /v0/purl`` and ``POST /v0/orgs/{slug}/purl``) defaults
        to **fail-open**: any input purl whose resolution/analysis has not finished is
        **silently omitted** from the response. A naive caller therefore cannot tell
        "this version is clean" apart from "this version was dropped from the response".
        The parameters below opt into the server behaviors that make omissions visible.

        Args:
            license: ``"true"``/``"false"`` — request license information (stringly-typed
                to match the query param the API expects).
            components: list of component dicts to score, e.g. ``[{"purl": "pkg:npm/lodash@4.18.1"}]``.
            org_slug: organization slug. When provided, routes to the org-scoped endpoint
                ``POST /v0/orgs/{org_slug}/purl``; otherwise the deprecated ``POST /v0/purl``.
            poll: opt into a fail-closed bounded wait for pending analysis (``poll=True`` →
                ``poll=true`` query param). ``None`` omits the param (server default).
            timeout_sec: bound in seconds for the ``poll`` wait (``→ timeoutSec``). The
                server may cap this via a feature flag. ``None`` omits the param.
            alerts: when ``True`` (``→ alerts=true``), the server emits synthetic
                ``pendingScan``/``notFound`` status rows instead of silently omitting
                unresolved inputs, so callers can distinguish "no data yet" from "clean".
            purl_errors: when ``True`` (``→ purlErrors``), the server includes per-purl
                error rows for malformed/unresolvable inputs. ``None`` omits the param.
                For backward compatibility, legacy string values passed to the promoted
                Boolean parameters are forwarded unchanged.
            strict: client-side guard. When ``True``, compares the exact ``purl`` string
                of each requested component against the returned ``inputPurl`` (or the
                ``purl`` fallback). The API defines ``inputPurl`` as the original,
                unmodified input before server normalization, so canonicalized ``purl``
                values do not cause false omissions. Raises
                :class:`~socketdev.exceptions.APIPartialResponse` (with a ``missing``
                list) if any requested purl is absent from the response. This surfaces
                partial batches even without ``alerts=True``. Only components that carry
                a ``purl`` string are checked.
            **kwargs: forwarded verbatim into the query string (back-compat passthrough for
                any params not yet promoted to first-class arguments).

        Returns:
            A deduped list of result rows. When ``alerts=True``, unresolved inputs appear
            as synthetic rows carrying ``pendingScan``/``notFound`` alerts rather than being
            omitted. On a non-200 response, logs the error and returns ``[]`` (callers that
            need to fail closed should treat ``[]`` as an error).

        Raises:
            APIPartialResponse: if ``strict=True`` and one or more requested component purls
                are missing from the response.
        """
        if org_slug is None:
            warnings.warn(
                "Calling purl.post() without org_slug uses the deprecated POST /v0/purl endpoint. "
                "Pass org_slug to migrate to POST /v0/orgs/{org_slug}/purl.",
                DeprecationWarning,
                stacklevel=2,
            )
        path = f"orgs/{org_slug}/purl?" if org_slug else "purl?"
        if components is None:
            components = []
        purls = {"components": components}
        purls = json.dumps(purls)
        query_args = {
            "license": license,
        }
        # Promote the typed params into query args only when explicitly set, so existing
        # callers keep the server's fail-open default (None => omit the param entirely).
        if poll is not None:
            query_args["poll"] = _encode_bool_query_value(poll)
        if timeout_sec is not None:
            query_args["timeoutSec"] = str(timeout_sec)
        if alerts is not None:
            query_args["alerts"] = _encode_bool_query_value(alerts)
        if purl_errors is not None:
            query_args["purlErrors"] = _encode_bool_query_value(purl_errors)
        if kwargs:
            query_args.update(kwargs)
        params = urllib.parse.urlencode(query_args)
        path += params
        response = self.api.do_request(path=path, payload=purls, method="POST")
        if response.status_code == 200:
            artifact_rows = []
            stream_records = []
            result = response.text
            result = result.strip('"').strip()
            for line in result.split("\n"):
                if line and line != '"':
                    try:
                        item = json.loads(line)
                        if isinstance(item, dict) and item.get("_type") in {
                            "purlError",
                            "summary",
                        }:
                            stream_records.append(item)
                        else:
                            artifact_rows.append(item)
                    except json.JSONDecodeError:
                        continue
            purl_deduped = Dedupe.dedupe(artifact_rows, batched=True)
            purl_deduped.extend(stream_records)
            if strict:
                self._raise_on_missing(components, purl_deduped)
            return purl_deduped

        log.error(f"Error posting {components} to the Purl API: {response.status_code}")
        log.error(response.text)
        return []

    @staticmethod
    def _raise_on_missing(components: list, results: list) -> None:
        """Raise APIPartialResponse if any requested component purl is absent from results.

        Only components exposing a ``purl`` string are checked. The batch API contract
        defines ``inputPurl`` as the original, unmodified input string before server-side
        normalization, so matching it exactly preserves the caller's identity even when
        the response's canonical ``purl`` differs. ``purl`` is retained as a fallback,
        and typed ``purlError`` stream records carry ``inputPurl`` under ``value``.
        """
        requested = [
            c["purl"]
            for c in components
            if isinstance(c, dict) and isinstance(c.get("purl"), str)
        ]
        if not requested:
            return
        returned = set()
        for row in results:
            if not isinstance(row, dict):
                continue
            for field in ("inputPurl", "purl"):
                value = row.get(field)
                if isinstance(value, str):
                    returned.add(value)
            record_value = row.get("value")
            if isinstance(record_value, dict):
                input_purl = record_value.get("inputPurl")
                if isinstance(input_purl, str):
                    returned.add(input_purl)
        missing = [purl for purl in requested if purl not in returned]
        if missing:
            raise APIPartialResponse(
                "purl.post(strict=True): the batch response omitted "
                f"{len(missing)} of {len(requested)} requested purls "
                "(fail-open: unresolved inputs are dropped unless alerts=True/poll=True): "
                f"{missing}",
                missing=missing,
            )
