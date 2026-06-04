"""Lane 2 Type-Tone-Goldstein (TTG) archive — Phase-2 REAL fetch path.

This is the reviewed code module that ADDS the real GDELT network fetch path
the Phase-1 scaffold deliberately omitted. The real fetch is present here so a
future reviewer can byte-review it — but it is DISABLED by a source-level gate
and cannot be enabled by any runtime configuration.

═══════════════════════════════════════════════════════════════════════════════
NON-RUNTIME SOURCE GATE
═══════════════════════════════════════════════════════════════════════════════
`REAL_FETCH_SOURCE_GATE_ENABLED` ships ``False``. Enabling the real GDELT fetch
requires EDITING THAT LINE in this source file (a reviewed code change) AND a
separate, explicit execution authorization. It is intentionally NOT read from:
  - any environment variable,
  - any CLI flag,
  - any config file or local settings file,
  - any function parameter / default parameter,
  - any other one-line runtime switch.
No runtime configuration can flip it. With the gate ``False`` (as shipped), the
real fetch entrypoint HARD-ERRORS before constructing a URL, before importing
any network library, and before opening any connection. The runtime three-guard
build gate (module constant + CLI flag + env var) controls whether the *build
run* proceeds at all; it does NOT, and cannot, enable the network.

This module:
  - performs NO real network contact when imported or when the shipped gate is
    in force;
  - retains ONLY the five approved fields via the pure logic in
    `lane2_type_tone_goldstein_local_archive`;
  - is value-blind (structural / provenance metadata only);
  - touches NO market / outcome / join / 2023+ data and computes NO TTG
    feature or statistic.

Running a real build requires (a) editing the source gate below, (b) a separate
explicit execution-authorization prompt, and (c) the codebook/availability
preconditions — none of which are granted by importing or testing this module.
"""

from __future__ import annotations

import json
import os
from datetime import date
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence

import lane2_type_tone_goldstein_local_archive as archive

# ═════════════════════════════════════════════════════════════════════════════
# SOURCE-LEVEL REAL-FETCH GATE — edit-to-enable only. NOT runtime-configurable.
# Do NOT wire this to os.environ, argparse, a config file, or a parameter.
REAL_FETCH_SOURCE_GATE_ENABLED = False
# ═════════════════════════════════════════════════════════════════════════════

# Exact, frozen real-fetch refusal message. Tests assert string equality.
REAL_FETCH_BLOCK_MESSAGE = (
    "REAL GDELT FETCH NOT AUTHORIZED: source gate "
    "REAL_FETCH_SOURCE_GATE_ENABLED is False. Enabling requires a reviewed "
    "source edit AND a separate execution authorization; it is not reachable "
    "via env var, CLI flag, config file, settings file, or parameter."
)

# GDELT 1.0 Event daily-update download base. The file-DOWNLOAD URL built from
# this base is provenance metadata (allowed in the manifest). It is a different
# namespace from the row-level GDELT `SOURCEURL` field (codebook idx 57), which
# is forbidden and never retained as a row column.
GDELT1_EVENT_BASE_URL = "http://data.gdeltproject.org/events/"

REAL_FETCH_TIMEOUT_SECONDS = 60

# Approved positional indices, independently re-derived from the committed
# codebook reference (docs/lane2_gdelt1_event_codebook_reference_v0.1.md,
# content SHA-256 3c5fa5bc054fbefaea2a26f9700ee827f2ff86a059d1625ffa127b10bf035a58):
# SQLDATE -> py idx 1, QuadClass -> 29, GoldsteinScale -> 30, NumMentions -> 31,
# AvgTone -> 34. The build verifies the module constants against this map and
# fails closed on mismatch (archive.assert_codebook_indices).
CANONICAL_CODEBOOK_DERIVED_INDICES: Dict[str, int] = {
    "sqldate": 1,
    "quadclass": 29,
    "goldsteinscale": 30,
    "nummentions": 31,
    "avgtone": 34,
}


class RealFetchNotAuthorized(archive.ArchiveBoundaryError):
    """Raised by the real fetch entrypoint while the source gate is False.

    Message is exactly `REAL_FETCH_BLOCK_MESSAGE`."""


# ── Provenance URL (file-download namespace, distinct from row SOURCEURL) ────

def build_source_file_url(source_file_date: date) -> str:
    """Build the file-download URL for a GDELT daily update file. This is the
    file-download URL (provenance metadata), NOT the row-level `SOURCEURL`
    field. The two namespaces are kept strictly separate.
    """
    name = archive.SOURCE_FILE_NAME_TEMPLATE.format(
        yyyymmdd=source_file_date.strftime("%Y%m%d")
    )
    return GDELT1_EVENT_BASE_URL + name


# ── Real fetch entrypoint (gated; hard-errors before any URL open) ───────────

def fetch_one_source_file(
    source_file_date: date,
    source_file_url: Optional[str] = None,
) -> bytes:
    """Real GDELT fetch entrypoint for one daily source file.

    Order of operations is load-bearing:
      1. CHECK THE SOURCE GATE FIRST. If `REAL_FETCH_SOURCE_GATE_ENABLED` is
         False (as shipped), raise `RealFetchNotAuthorized` immediately — before
         building any URL, before importing any network library, before opening
         any connection.
      2. (Only if the gate is enabled by a future source edit) re-assert the
         authorized source-file window / 2023+ seal on `source_file_date`.
      3. Build the download URL and open it via `_open_url`.

    The gate is checked unconditionally and is not influenced by any argument,
    environment variable, or config. No parameter can bypass it.
    """
    if not REAL_FETCH_SOURCE_GATE_ENABLED:
        raise RealFetchNotAuthorized(REAL_FETCH_BLOCK_MESSAGE)
    # --- Below is reachable only after a reviewed source edit + future auth. ---
    if not (archive.WINDOW_START <= source_file_date <= archive.WINDOW_END):
        raise archive.Post2022SealBreach(
            "source file date {} outside authorized window".format(
                source_file_date.isoformat()
            )
        )
    if source_file_url is None:
        source_file_url = build_source_file_url(source_file_date)
    return _open_url(source_file_url)


def _open_url(url: str, _opener: Optional[Any] = None) -> bytes:
    """Open a URL and return its bytes. Reached ONLY after the source gate has
    been enabled by a reviewed source edit. The network library is imported
    lazily here — so when the gate is False (shipped), no network library is
    imported at all. `_opener` is a future test seam; the shipped gate prevents
    this function from ever being reached in this dispatch.
    """
    import urllib.request  # lazy: only after the source gate passes

    opener = _opener if _opener is not None else urllib.request.build_opener()
    with opener.open(url, timeout=REAL_FETCH_TIMEOUT_SECONDS) as resp:
        return resp.read()


# ── Phase-2 build orchestration (network-free; injected fetcher) ─────────────

def run_phase2_archive_build(
    candidate_dates: Sequence[str],
    out_dir: str,
    *,
    cli_flag: bool = False,
    module_authorized: Optional[bool] = None,
    env: Optional[Mapping[str, str]] = None,
    fetch_callable: Optional[Callable[..., bytes]] = None,
    codebook_derived_indices: Optional[Mapping[str, int]] = None,
    route_edge_incomplete: bool = False,
    is_zip: bool = False,
) -> Dict[str, Any]:
    """Orchestrate a Phase-2 archive build.

    Sequence:
      1. Verify codebook indices (fail closed on mismatch) — before any fetch.
      2. Three-guard run gate (module constant + CLI flag + env). Refuse if not
         all satisfied — before enumeration / fetch.
      3. Enumerate the source-file universe (2023+ and pre-window dates
         hard-error at enumeration, before any open).
      4. For each in-window source-file date: fetch bytes via `fetch_callable`
         (default = the gated real fetch, which hard-errors), classify rows by
         availability eligibility + window coverage, accumulate retained rows
         and value-agnostic per-file provenance.
      5. Write the approved-fields archive + a value-agnostic provenance
         manifest under `out_dir`.

    `fetch_callable(source_file_date: date, source_file_url: str) -> bytes` is a
    seam so synthetic tests can inject a non-network fetcher. The DEFAULT is the
    gated real fetch, which hard-errors before any URL open. This function
    performs no network access itself.
    """
    # 1. Codebook index verification — fail closed before anything else.
    archive.assert_codebook_indices(
        codebook_derived_indices
        if codebook_derived_indices is not None
        else CANONICAL_CODEBOOK_DERIVED_INDICES
    )

    # 2. Three-guard run gate.
    if not archive.guards_satisfied(
        cli_flag, module_authorized=module_authorized, env=env
    ):
        raise archive.ArchiveBuildRefused(archive.REFUSAL_MESSAGE)

    # 3. Enumerate (2023+ / pre-window hard-error at enumeration).
    universe = archive.enumerate_source_universe(candidate_dates or [])

    fetch = fetch_callable if fetch_callable is not None else fetch_one_source_file

    retained_rows: List[Dict[str, str]] = []
    per_file_provenance: List[Dict[str, Any]] = []
    edge_incomplete_days: set = set()

    for iso in universe:
        f_date = date.fromisoformat(iso)
        url = build_source_file_url(f_date)
        # Default `fetch` is the gated real fetch: it raises RealFetchNotAuthorized
        # here, aborting the build before any network contact.
        payload = fetch(f_date, url)
        byte_hash = archive.sha256_hex(payload)
        cls = archive.classify_payload_rows(
            payload,
            source_file_date=f_date,
            is_zip=is_zip,
            route_edge_incomplete=route_edge_incomplete,
        )
        retained_rows.extend(cls.retained_rows)
        if cls.dropped_by_reason.get(archive.DROP_REASON_EDGE_WINDOW_EXCLUSION, 0):
            edge_incomplete_days.add(iso)
        per_file_provenance.append(
            archive.build_per_file_provenance_entry(
                source_file_date=f_date,
                source_file_url=url,
                attempted=True,
                opened=True,
                classification=cls,
                byte_hash=byte_hash,
                byte_size=len(payload),
                error_status=None,
            )
        )

    os.makedirs(out_dir, exist_ok=True)
    archive_path = os.path.join(out_dir, "ttg_approved_fields_archive.csv")
    artifact = archive.write_approved_archive_csv(retained_rows, archive_path)

    manifest = archive.build_phase2_provenance_manifest(
        source_file_window={
            "start": archive.WINDOW_START.isoformat(),
            "end": archive.WINDOW_END.isoformat(),
            "enumeration": "deterministic YYYYMMDD per-day; no 2023+; no pre-window",
        },
        per_file_provenance=per_file_provenance,
        archive_artifacts=[artifact],
        total_retained_row_count=len(retained_rows),
        edge_incomplete_day_count=len(edge_incomplete_days),
    )
    manifest_path = os.path.join(out_dir, "ttg_archive_provenance_manifest.json")
    with open(manifest_path, "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=False)

    return {
        "manifest": manifest,
        "manifest_path": manifest_path,
        "archive_artifact": artifact,
        "universe": universe,
    }
