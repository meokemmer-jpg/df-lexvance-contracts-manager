
# K12+K13+K16 Trinity-CONTRARIAN 2026-05-17 (Cross-LLM-validated)
def k12_provenance(payload: bytes, key: bytes = b"df-trinity-contrarian-v1") -> dict:
    import hashlib, hmac
    return {
        "payload_hash": hashlib.sha256(payload).hexdigest(),
        "hmac_sha256": hmac.new(key, payload, hashlib.sha256).hexdigest(),
    }

def k13_anchor(payload_hash: str) -> dict:
    from datetime import datetime, timezone
    return {
        "anchor_type": "rfc3161-mock",
        "iso_ts": datetime.now(timezone.utc).isoformat(),
        "payload_hash": payload_hash,
    }

def k16_lock_or_exit(df_name: str):
    import fcntl, os, sys
    lock_path = f"/tmp/df-trinity-{df_name}.lock"
    fd = os.open(lock_path, os.O_CREAT | os.O_WRONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fd
    except BlockingIOError:
        sys.exit(3)

"""DF-LEXVANCE-CONTRACTS-MANAGER Engine [CRUX-MK].

Welle-48 Track-A Wave-1 DC-1 Foundation-DF (Gap-Cluster C).
Vertragsmanagement ueber 6 Kategorien (B2B/AGB/NDA/Lizenz/HR/M&A).

ENV-Var-gated Default-Disabled. Mock-Fallback bei Real-Mode-Disabled.

Pre/Post-Conditions:
- Pre: vertrag_id (str), kategorie (str in VERTRAGS_KATEGORIEN)
- Post: ContractsAuditResult mit klausel_findings, agb_kontrolle_status, ip_compliance_status
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


# 6 Pflicht-Vertrags-Kategorien
VERTRAGS_KATEGORIEN = ("B2B_MSA", "AGB", "NDA", "LIZENZ", "HR", "MA")

# Pflicht-Klauseln pro Kategorie (Skelett, Welle-49+ erweitert)
PFLICHT_KLAUSELN = {
    "B2B_MSA": ("haftung", "datenschutz_dpa", "sla", "kuendigung", "subprozessoren"),
    "AGB": ("widerruf", "haftungs_ausschluss", "gerichtsstand", "geltungsbereich"),  # §§ 305-310 BGB
    "NDA": ("vertraulichkeit", "dauer", "ausnahmen", "rueckgabe"),
    "LIZENZ": ("scope", "exclusivity", "lizenzgebuehr", "oss_compliance"),
    "HR": ("verguetung", "kuendigung", "wettbewerbsverbot", "datenschutz"),
    "MA": ("kaufpreis", "warranties", "closing_conditions", "earn_out", "mac_clause"),
}


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ContractsAuditResult:
    """Pflicht-Felder per env-var-gated-real-integration-default.md Property-3."""
    vertrag_id: str
    kategorie: str
    klausel_findings: tuple       # Liste gefundener Klauseln
    fehlende_pflicht_klauseln: tuple
    agb_kontrolle_status: str     # "PASS"|"FAIL"|"NOT_APPLICABLE"
    ip_compliance_status: str     # "PASS"|"FAIL"|"NOT_APPLICABLE"
    source: str                   # "mock"|"real-api"
    iso_timestamp: str
    phronesis_ticket: Optional[str] = None
    warnings: tuple = field(default_factory=tuple)


def _check_pflicht_klauseln(kategorie: str, gefundene_klauseln: tuple) -> tuple:
    """Pre: kategorie in VERTRAGS_KATEGORIEN; Post: tuple fehlender Pflicht-Klauseln."""
    assert kategorie in VERTRAGS_KATEGORIEN, f"unknown kategorie: {kategorie}"
    pflicht = set(PFLICHT_KLAUSELN[kategorie])
    gefunden = set(gefundene_klauseln)
    return tuple(sorted(pflicht - gefunden))


def mock_contracts_audit(
    vertrag_id: str,
    kategorie: str = "B2B_MSA",
) -> ContractsAuditResult:
    """Mock-Audit: liefert leere Findings + alle Pflicht-Klauseln als fehlend."""
    assert vertrag_id, "vertrag_id required"
    fehlend = _check_pflicht_klauseln(kategorie, ())
    return ContractsAuditResult(
        vertrag_id=vertrag_id,
        kategorie=kategorie,
        klausel_findings=(),
        fehlende_pflicht_klauseln=fehlend,
        agb_kontrolle_status="NOT_APPLICABLE" if kategorie != "AGB" else "FAIL",
        ip_compliance_status="NOT_APPLICABLE" if kategorie != "LIZENZ" else "FAIL",
        source="mock",
        iso_timestamp=iso_now(),
        phronesis_ticket=None,
        warnings=("MOCK_MODE_NO_REAL_KLAUSEL_DISCOVERY",),
    )


def real_contracts_audit(
    vertrag_id: str,
    kategorie: str = "B2B_MSA",
    klauseln_aus_df101: Optional[tuple] = None,
    phronesis_ticket: Optional[str] = None,
) -> ContractsAuditResult:
    """Real-Mode (NUR mit PHRONESIS_TICKET fuer M&A; sonst graceful Fallback)."""
    assert vertrag_id, "vertrag_id required"
    # M&A erzwingt PHRONESIS_TICKET (K_0-naehe)
    if kategorie == "MA":
        if not phronesis_ticket:
            phronesis_ticket = os.environ.get("PHRONESIS_TICKET")
        if not phronesis_ticket:
            return mock_contracts_audit(vertrag_id, kategorie)
    gefunden = klauseln_aus_df101 or ()
    fehlend = _check_pflicht_klauseln(kategorie, gefunden)
    return ContractsAuditResult(
        vertrag_id=vertrag_id,
        kategorie=kategorie,
        klausel_findings=gefunden,
        fehlende_pflicht_klauseln=fehlend,
        agb_kontrolle_status="PASS" if (kategorie != "AGB" or not fehlend) else "FAIL",
        ip_compliance_status="PASS" if (kategorie != "LIZENZ" or not fehlend) else "FAIL",
        source="real-api",
        iso_timestamp=iso_now(),
        phronesis_ticket=phronesis_ticket,
        warnings=(),
    )


def dispatch_contracts_audit(
    vertrag_id: str,
    kategorie: str = "B2B_MSA",
) -> ContractsAuditResult:
    """Dispatcher mit ENV-Var-Gating."""
    real_enabled = os.environ.get("DF_LEXVANCE_CONTRACTS_REAL_ENABLED", "").lower() == "true"
    if real_enabled:
        return real_contracts_audit(vertrag_id, kategorie)
    return mock_contracts_audit(vertrag_id, kategorie)


def has_pflicht_klausel_gaps(result: ContractsAuditResult) -> bool:
    """Pre: result valid; Post: True iff Pflicht-Klauseln fehlen."""
    return len(result.fehlende_pflicht_klauseln) > 0


def to_audit_record(result: ContractsAuditResult) -> dict:
    return {
        "ts": result.iso_timestamp,
        "df": "DF-LEXVANCE-CONTRACTS-MANAGER",
        "vertrag_id": result.vertrag_id,
        "kategorie": result.kategorie,
        "fehlende_klauseln_count": len(result.fehlende_pflicht_klauseln),
        "agb_status": result.agb_kontrolle_status,
        "ip_status": result.ip_compliance_status,
        "source": result.source,
        "phronesis_ticket": result.phronesis_ticket or "none",
    }
