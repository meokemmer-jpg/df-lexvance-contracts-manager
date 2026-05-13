"""Basic Tests fuer DF-LEXVANCE-CONTRACTS-MANAGER [CRUX-MK]."""
from __future__ import annotations

import os
import sys
import pathlib
import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.engine import (
    VERTRAGS_KATEGORIEN, PFLICHT_KLAUSELN,
    ContractsAuditResult,
    mock_contracts_audit, real_contracts_audit, dispatch_contracts_audit,
    has_pflicht_klausel_gaps, to_audit_record, _check_pflicht_klauseln,
)


def _clear_env(monkeypatch):
    monkeypatch.delenv("DF_LEXVANCE_CONTRACTS_REAL_ENABLED", raising=False)
    monkeypatch.delenv("PHRONESIS_TICKET", raising=False)


def test_default_mock_no_env(monkeypatch):
    _clear_env(monkeypatch)
    result = dispatch_contracts_audit("V-001", "B2B_MSA")
    assert result.source == "mock"
    assert result.klausel_findings == ()
    assert len(result.fehlende_pflicht_klauseln) > 0  # alle fehlen


def test_env_true_with_ma_phronesis(monkeypatch):
    """M&A erzwingt PHRONESIS_TICKET."""
    _clear_env(monkeypatch)
    monkeypatch.setenv("DF_LEXVANCE_CONTRACTS_REAL_ENABLED", "true")
    monkeypatch.setenv("PHRONESIS_TICKET", "PT-W48-MA-001")
    result = dispatch_contracts_audit("V-MA-001", "MA")
    assert result.source == "real-api"
    assert result.phronesis_ticket == "PT-W48-MA-001"


def test_ma_without_phronesis_fallback(monkeypatch):
    """M&A ohne PHRONESIS_TICKET → graceful Fallback zu mock (K_0-Schutz)."""
    _clear_env(monkeypatch)
    monkeypatch.setenv("DF_LEXVANCE_CONTRACTS_REAL_ENABLED", "true")
    result = dispatch_contracts_audit("V-MA-002", "MA")
    assert result.source == "mock", "M&A ohne PHRONESIS muss fallback ausloesen"


def test_b2b_msa_without_phronesis_works(monkeypatch):
    """B2B_MSA braucht KEIN PHRONESIS_TICKET (nur M&A)."""
    _clear_env(monkeypatch)
    monkeypatch.setenv("DF_LEXVANCE_CONTRACTS_REAL_ENABLED", "true")
    result = dispatch_contracts_audit("V-B2B-001", "B2B_MSA")
    assert result.source == "real-api"


def test_conservation_6_kategorien_pflicht_klauseln():
    """Conservation: alle 6 Kategorien haben Pflicht-Klauseln definiert."""
    assert len(VERTRAGS_KATEGORIEN) == 6
    for kat in VERTRAGS_KATEGORIEN:
        assert kat in PFLICHT_KLAUSELN
        assert len(PFLICHT_KLAUSELN[kat]) >= 3, f"Kategorie {kat} hat zu wenige Pflicht-Klauseln"


def test_check_pflicht_klauseln_full_coverage():
    """Wenn alle Pflicht-Klauseln gefunden → keine fehlenden."""
    pflicht = PFLICHT_KLAUSELN["B2B_MSA"]
    fehlend = _check_pflicht_klauseln("B2B_MSA", pflicht)
    assert fehlend == ()


def test_unknown_kategorie_raises():
    with pytest.raises(AssertionError):
        _check_pflicht_klauseln("UNKNOWN_KAT", ())


def test_has_pflicht_klausel_gaps():
    result = mock_contracts_audit("V-X", "AGB")
    assert has_pflicht_klausel_gaps(result), "Mock-Audit hat alle Pflicht-Klauseln fehlend"


def test_audit_record_format():
    result = mock_contracts_audit("V-AUD", "B2B_MSA")
    rec = to_audit_record(result)
    assert {"ts", "df", "vertrag_id", "kategorie", "fehlende_klauseln_count", "source"} <= set(rec.keys())
    assert rec["df"] == "DF-LEXVANCE-CONTRACTS-MANAGER"
