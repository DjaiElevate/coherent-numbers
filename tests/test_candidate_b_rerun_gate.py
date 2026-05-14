"""Tests for the deterministic rerun gate (section 14 enforcement)."""

import hashlib

import numpy as np
import pytest

from candidate_b_rerun_gate import (
    RerunInconsistency,
    assert_byte_identical_reruns,
    canonicalize_protocol_payload,
    payload_digest,
)


def test_canonical_form_sorts_keys():
    a = {"b": 1, "a": 2, "c": 3}
    b = {"c": 3, "a": 2, "b": 1}
    assert canonicalize_protocol_payload(a) == canonicalize_protocol_payload(b)


def test_canonical_form_handles_numpy_scalars():
    payload = {
        "x": np.int64(5),
        "y": np.float64(0.25),
        "flag": np.bool_(True),
    }
    bytes_canonical = canonicalize_protocol_payload(payload)
    # Equivalent plain Python payload must produce the same canonical bytes
    plain = {"x": 5, "y": 0.25, "flag": True}
    assert bytes_canonical == canonicalize_protocol_payload(plain)


def test_canonical_form_handles_numpy_arrays():
    payload = {"v": np.array([1.0, 2.0, 3.0])}
    bytes_canonical = canonicalize_protocol_payload(payload)
    plain = {"v": [1.0, 2.0, 3.0]}
    assert bytes_canonical == canonicalize_protocol_payload(plain)


def test_canonical_form_rejects_nan():
    with pytest.raises(ValueError):
        canonicalize_protocol_payload({"x": float("nan")})


def test_canonical_form_rejects_infinity():
    with pytest.raises(ValueError):
        canonicalize_protocol_payload({"x": float("inf")})


def test_canonical_form_rejects_numpy_nan():
    with pytest.raises(ValueError):
        canonicalize_protocol_payload({"x": np.float64("nan")})


def test_canonical_form_stable_across_dict_insertion_order():
    a = {}
    a["z"] = 1
    a["a"] = 2
    b = {}
    b["a"] = 2
    b["z"] = 1
    assert canonicalize_protocol_payload(a) == canonicalize_protocol_payload(b)


def test_payload_digest_is_deterministic():
    payload = {"alpha": 1.0, "beta": [1, 2, 3], "gamma": {"x": True}}
    d1 = payload_digest(payload)
    d2 = payload_digest(payload)
    assert d1 == d2
    assert len(d1) == 64


def test_assert_byte_identical_reruns_passes_when_deterministic():
    calls = [0]

    def fixed_callable():
        calls[0] += 1
        return {"observed_pss_b1": 0.125, "verdict": "Non-confirmatory"}

    canonical = assert_byte_identical_reruns(fixed_callable)
    assert calls[0] == 2
    digest = hashlib.sha256(canonical).hexdigest()
    assert len(digest) == 64


def test_assert_byte_identical_reruns_raises_on_perturbation():
    state = {"n": 0}

    def perturbed():
        state["n"] += 1
        return {"x": float(state["n"])}

    with pytest.raises(RerunInconsistency):
        assert_byte_identical_reruns(perturbed)


def test_assert_byte_identical_reruns_calls_exactly_twice_on_match():
    state = {"calls": 0}

    def fixed():
        state["calls"] += 1
        return {"a": 1}

    assert_byte_identical_reruns(fixed)
    assert state["calls"] == 2


def test_canonical_form_rejects_unsupported_type():
    class Unsupported:
        pass

    with pytest.raises(TypeError):
        canonicalize_protocol_payload({"x": Unsupported()})
