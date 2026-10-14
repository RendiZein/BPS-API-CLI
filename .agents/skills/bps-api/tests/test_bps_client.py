#!/usr/bin/env python3
"""
Unit and Integration Tests for BPSClient
----------------------------------------
Runs with standard unittest: `python -m unittest tests/test_bps_client.py`
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from bps_client import BPSClient, format_table, export_csv


class TestBPSClientUnit(unittest.TestCase):
    def setUp(self):
        self.dummy_client = BPSClient(
            api_key="mock_key_12345",
            version="v1",
            base_url="https://webapi.bps.go.id",
            default_domain="0000",
            default_lang="ind",
        )

    def test_url_builder(self):
        """Test URL path segment construction."""
        url = self.dummy_client._build_url(
            action="list",
            segments=[("model", "subject"), ("domain", "0000"), ("page", 1)],
        )
        expected = "https://webapi.bps.go.id/v1/api/list/model/subject/domain/0000/page/1/key/mock_key_12345/"
        self.assertEqual(url, expected)

    def test_unwrap_list_response_valid(self):
        """Test unwrapping standard BPS 2-element list response."""
        mock_resp = {
            "status": "OK",
            "data-availability": "available",
            "data": [
                {"page": 1, "pages": 5, "total": 50},
                [{"id": 1, "title": "Subjek A"}, {"id": 2, "title": "Subjek B"}],
            ],
        }
        pag, items = self.dummy_client._unwrap_list_response(mock_resp)
        self.assertEqual(pag["total"], 50)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["title"], "Subjek A")

    def test_unwrap_list_response_empty_string(self):
        """Test handling of BPS quirk: data returned as empty string."""
        mock_resp = {
            "status": "OK",
            "data-availability": "list-not-available",
            "data": "",
        }
        pag, items = self.dummy_client._unwrap_list_response(mock_resp)
        self.assertEqual(items, [])
        self.assertEqual(pag.get("total"), 0)

    def test_decode_dynamic_data(self):
        """Test decoding composite keys in datacontent."""
        mock_dynamic_response = {
            "status": "OK",
            "labelvervar": "Komoditas",
            "var": [{"val": 101, "label": "Produksi", "unit": "Ton"}],
            "vervar": [{"val": 1, "label": "Padi"}, {"val": 2, "label": "Jagung"}],
            "turvar": [{"val": 0, "label": "Total"}],
            "tahun": [{"val": 120, "label": "2020"}],
            "turtahun": [{"val": 0, "label": "Tahunan"}],
            "datacontent": {
                "110101200": 54000.5,
                "210101200": 21000.2,
            },
        }

        decoded = self.dummy_client.decode_dynamic_data(mock_dynamic_response)
        self.assertEqual(len(decoded), 2)

        padi = next(r for r in decoded if r["Komoditas"] == "Padi")
        self.assertEqual(padi["Nilai"], 54000.5)
        self.assertEqual(padi["Variabel"], "Produksi")
        self.assertEqual(padi["Satuan"], "Ton")
        self.assertEqual(padi["Tahun"], "2020")

    def test_csv_export(self):
        """Test CSV export formatting."""
        rows = [
            {"Wilayah": "Pusat", "Nilai": 100},
            {"Wilayah": "Jabar", "Nilai": 200},
        ]
        csv_str = export_csv(rows)
        self.assertIn("Wilayah,Nilai", csv_str)
        self.assertIn("Pusat,100", csv_str)
        self.assertIn("Jabar,200", csv_str)


class TestBPSClientLive(unittest.TestCase):
    """Live API integration tests against BPS server."""
    @classmethod
    def setUpClass(cls):
        try:
            cls.client = BPSClient()
        except Exception:
            raise unittest.SkipTest("BPS_API_KEY not configured for live tests.")

    def test_live_domain_prov(self):
        provs = self.client.get_domains(domain_type="prov")
        self.assertGreater(len(provs), 30)
        self.assertTrue(any(p["domain_id"] == "3200" for p in provs))

    def test_live_indicators(self):
        pag, indicators = self.client.get_indicators()
        self.assertGreater(len(indicators), 5)
        self.assertTrue(any("inflasi" in i["title"].lower() for i in indicators))


if __name__ == "__main__":
    unittest.main()
