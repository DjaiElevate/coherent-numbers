"""Deterministic rerun gate for Candidate B (section 14 of the design memo).

The gate canonicalizes the protocol payload — the deterministic numeric
output of `candidate_b_protocol.run` — and compares two independent
invocations at the byte level. Volatile metadata (timestamps, paths, current
HEAD) does NOT enter the canonical form; it lives in the verdict-log header
which is composed outside the protocol module.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Callable

import numpy as np


class RerunInconsistency(RuntimeError):
    """Raised when two protocol invocations produce divergent canonical payloads."""


def _canonical_value(value: Any) -> Any:
    if isinstance(value, bool):
        return bool(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, (int,)):
        return int(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError("non-finite float in protocol payload: {}".format(value))
        return value
    if isinstance(value, np.floating):
        f = float(value)
        if f != f or f in (float("inf"), float("-inf")):
            raise ValueError("non-finite float in protocol payload: {}".format(f))
        return f
    if isinstance(value, np.ndarray):
        return [_canonical_value(x) for x in value.tolist()]
    if isinstance(value, (list, tuple)):
        return [_canonical_value(x) for x in value]
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            out[str(k)] = _canonical_value(v)
        return out
    if value is None:
        return None
    if isinstance(value, str):
        return value
    raise TypeError(
        "unsupported type in protocol payload: {}".format(type(value).__name__)
    )


def canonicalize_protocol_payload(payload: Any) -> bytes:
    """Return a deterministic byte encoding of *payload*.

    Sorted keys, compact separators, ASCII-only. NaN and infinity are
    explicitly rejected so canonical form can never become ambiguous.
    """
    safe = _canonical_value(payload)
    return json.dumps(
        safe, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def payload_digest(payload: Any) -> str:
    """Return SHA-256 hex of `canonicalize_protocol_payload(payload)`."""
    return hashlib.sha256(canonicalize_protocol_payload(payload)).hexdigest()


def assert_byte_identical_reruns(run_callable: Callable[[], Any]) -> bytes:
    """Call *run_callable* twice; raise RerunInconsistency if outputs differ.

    Returns the canonical byte payload of the (verified-equal) result.
    """
    payload_a = run_callable()
    payload_b = run_callable()
    bytes_a = canonicalize_protocol_payload(payload_a)
    bytes_b = canonicalize_protocol_payload(payload_b)
    if bytes_a != bytes_b:
        digest_a = hashlib.sha256(bytes_a).hexdigest()
        digest_b = hashlib.sha256(bytes_b).hexdigest()
        raise RerunInconsistency(
            "two protocol runs produced divergent canonical payload digests: "
            "{} vs {}".format(digest_a, digest_b)
        )
    return bytes_a
