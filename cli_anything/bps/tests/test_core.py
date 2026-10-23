"""
Synthetic Unit Tests for BPS CLI Harness.
Requires zero network connection — uses synthetic data and local SQLite/JSON mocks.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pytest

from cli_anything.bps.core.api import BPSClient
from cli_anything.bps.core.audit import audit_topic
from cli_anything.bps.core.cache import BPSCache
from cli_anything.bps.core.preview import PreviewProtocol, compute_statistics, fingerprint_data
from cli_anything.bps.core.session import SessionState, SessionStore, _locked_save_json


class FakeBPSClient(BPSClient):
    """Synthetic mock client simulating BPS API responses without network."""

    def __init__(self):
        self.api_key = "fake_key_12345"
        self.version = "v1"
        self.base_url = "https://webapi.bps.go.id"
        self.default_domain = "0000"
        self.default_lang = "ind"
        self.timeout = 5
        self.max_retries = 1

    def get_domains(self, domain_type: str = "all", prov=None):
        return [
            {"domain_id": "0000", "domain_name": "Indonesia", "domain_type": "all"},
            {"domain_id": "3500", "domain_name": "Provinsi Jawa Timur", "domain_type": "prov"},
            {"domain_id": "9400", "domain_name": "Provinsi Papua", "domain_type": "prov"},
        ]

    def get_subjects(self, domain=None, subcat=None, page=1):
        return (
            {"page": 1, "pages": 1, "total": 1, "count": 1},
            [{"sub_id": 23, "title": "Kemiskinan dan Ketimpangan", "subcat_id": 1}],
        )

    def get_variables(self, subject=None, domain=None, page=1, year=None, area=None):
        return (
            {"page": 1, "pages": 1, "total": 1, "count": 1},
            [{"var_id": 49, "title": "Persentase Penduduk Miskin", "unit": "Persen"}],
        )

    def get_periods(self, var_id: int, domain=None, page=1):
        return (
            {"page": 1, "pages": 1, "total": 2, "count": 2},
            [{"th_id": 126, "th": "2026"}, {"th_id": 125, "th": "2025"}],
        )

    def get_press_releases(self, domain=None, keyword=None, month=None, year=None, page=1):
        return (
            {"page": 1, "pages": 1, "total": 1, "count": 1},
            [{"brs_id": 101, "title": "Profil Kemiskinan Maret 2026", "rl_date": "2026-07-01"}],
        )

    def get_dynamic_data(self, var_id, th_id, domain=None, turvar_id=None, vervar_id=None, turth_id=None):
        return {
            "status": "OK",
            "datacontent": {
                "14901260": "9.06",
                "24901260": "10.45",
                "34901260": "7.82",
            },
            "var": [{"val": "49", "label": "Persentase Penduduk Miskin", "unit": "Persen"}],
            "vervar": [
                {"val": "1", "label": "Wilayah Barat"},
                {"val": "2", "label": "Wilayah Timur"},
                {"val": "3", "label": "Wilayah Tengah"},
            ],
            "turvar": [{"val": "0", "label": "Total"}],
            "tahun": [{"val": "126", "label": "2026"}],
            "turtahun": [{"val": "0", "label": "Tahun"}],
        }


# =============================================================================
# Unit Tests
# =============================================================================
def test_session_state_and_store():
    with tempfile.TemporaryDirectory() as tmpdir:
        sess_path = Path(tmpdir) / "test_session.json"
        traj_path = Path(tmpdir) / "test_trajectory.json"
        store = SessionStore(session_path=sess_path, trajectory_path=traj_path)

        state = store.load()
        assert state.domain == "0000"

        # Record action and change domain
        store.record_snapshot(state, "change_domain", {"old": "0000", "new": "3500"})
        state.domain = "3500"
        store.save(state)

        # Reload
        reloaded = store.load()
        assert reloaded.domain == "3500"
        assert len(reloaded.history) == 1

        # Undo
        restored = store.undo(reloaded)
        assert reloaded.domain == "0000"
        assert len(reloaded.future) == 1

        # Redo
        re_applied = store.redo(reloaded)
        assert reloaded.domain == "3500"


def test_atomic_file_locking_windows():
    with tempfile.TemporaryDirectory() as tmpdir:
        target_file = Path(tmpdir) / "locked.json"
        data = {"key": "test_lock_windows", "status": "ok"}
        _locked_save_json(target_file, data)
        assert target_file.exists()
        loaded = json.loads(target_file.read_text(encoding="utf-8"))
        assert loaded["key"] == "test_lock_windows"


def test_composite_key_decoder():
    client = FakeBPSClient()
    raw = client.get_dynamic_data(var_id=49, th_id=126)
    decoded = client.decode_dynamic_data(raw)
    assert len(decoded) == 3
    assert decoded[0]["variabel"] == "Persentase Penduduk Miskin"
    assert decoded[0]["nilai"] == 9.06
    assert decoded[1]["nilai"] == 10.45


def test_preview_statistics():
    vals = [5.0, 10.0, 15.0, 20.0, 25.0]
    stats = compute_statistics(vals)
    assert stats["min"] == 5.0
    assert stats["max"] == 25.0
    assert stats["mean"] == 15.0
    assert stats["median"] == 15.0
    assert stats["std_dev"] > 0


def test_preview_protocol_cache():
    with tempfile.TemporaryDirectory() as tmpdir:
        protocol = PreviewProtocol(previews_dir=tmpdir)
        client = FakeBPSClient()

        # First run: uncached
        summary_1 = protocol.generate_preview_bundle(client=client, var_id=49, th_id=126, domain="3500")
        assert summary_1["_cached"] is False
        assert summary_1["shape"]["rows"] == 3

        # Second run: cached
        summary_2 = protocol.generate_preview_bundle(client=client, var_id=49, th_id=126, domain="3500")
        assert summary_2["_cached"] is True
        assert summary_2["bundle_id"] == summary_1["bundle_id"]


def test_local_sqlite_cache():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "cache.db"
        cache = BPSCache(db_path=db_path)

        domains = [
            {"domain_id": "0000", "domain_name": "Indonesia", "domain_type": "all"},
            {"domain_id": "3500", "domain_name": "Provinsi Jawa Timur", "domain_type": "prov"},
        ]
        count = cache.sync_domains(domains)
        assert count == 2

        # Fuzzy search
        res = cache.search_domain("Jawa Timur")
        assert res is not None
        assert res["domain_id"] == "3500"

        res_nick = cache.search_domain("jatim")
        assert res_nick is not None
        assert res_nick["domain_id"] == "3500"


def test_audit_papua_anomaly():
    client = FakeBPSClient()
    # Audit on Papua domain (9400)
    result = audit_topic(client=client, topic="kemiskinan", domain_query="9400")
    assert result["ok"] is True
    assert len(result["data_anomalies"]) > 0
    assert "Pemekaran Papua" in result["data_anomalies"][0]
    assert len(result["research_proposals"]) == 3
