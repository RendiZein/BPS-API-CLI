"""
Data Preview Protocol Engine for BPS Web API (preview-bundle/v1).
Generates lightweight summary statistics, data shapes, and samples with SHA-256 content-addressable caching,
preventing context window explosion when inspecting tabular datasets.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .api import BPSClient

PROTOCOL_VERSION = "preview-bundle/v1"
DEFAULT_PREVIEWS_DIR = Path("data") / "previews"


def fingerprint_data(data: Any) -> str:
    """Generate SHA-256 fingerprint for data payload."""
    serialized = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def compute_statistics(values: List[float]) -> Dict[str, Optional[float]]:
    """Compute summary statistics (min, max, mean, median, std_dev) safely."""
    if not values:
        return {"min": None, "max": None, "mean": None, "median": None, "std_dev": None}

    sorted_vals = sorted(values)
    n = len(sorted_vals)
    val_min = round(sorted_vals[0], 4)
    val_max = round(sorted_vals[-1], 4)
    val_mean = round(sum(sorted_vals) / n, 4)

    if n % 2 == 1:
        val_median = round(sorted_vals[n // 2], 4)
    else:
        val_median = round((sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2, 4)

    if n > 1:
        variance = sum((x - val_mean) ** 2 for x in sorted_vals) / (n - 1)
        val_std = round(math.sqrt(variance), 4)
    else:
        val_std = 0.0

    return {
        "min": val_min,
        "max": val_max,
        "mean": val_mean,
        "median": val_median,
        "std_dev": val_std,
    }


class PreviewProtocol:
    def __init__(self, previews_dir: Optional[str | Path] = None):
        self.previews_dir = Path(previews_dir) if previews_dir else DEFAULT_PREVIEWS_DIR

    def generate_preview_bundle(
        self,
        client: BPSClient,
        var_id: int,
        th_id: int | str,
        domain: Optional[str] = None,
        force_refresh: bool = False,
    ) -> Dict[str, Any]:
        """
        Generate or fetch cached preview bundle for a variable and period.
        Emits: manifest.json, summary.json, and sample.csv artifact.
        """
        dom = domain or client.default_domain
        cache_params = {
            "protocol": PROTOCOL_VERSION,
            "domain": dom,
            "var_id": var_id,
            "th_id": str(th_id),
        }
        bundle_hash = fingerprint_data(cache_params)[:16]
        bundle_dir = self.previews_dir / f"bndl_{bundle_hash}"
        summary_path = bundle_dir / "summary.json"
        manifest_path = bundle_dir / "manifest.json"

        # Check existing cached preview bundle
        if not force_refresh and summary_path.exists() and manifest_path.exists():
            try:
                with open(summary_path, "r", encoding="utf-8") as f:
                    cached_summary = json.load(f)
                cached_summary["_cached"] = True
                cached_summary["_bundle_dir"] = str(bundle_dir)
                return cached_summary
            except Exception:
                pass

        # Fetch live data and decode
        raw_resp = client.get_dynamic_data(var_id=var_id, th_id=th_id, domain=dom)
        decoded_rows = client.decode_dynamic_data(raw_resp)

        # Extract numeric values
        numeric_vals = []
        null_count = 0
        for r in decoded_rows:
            v = r.get("nilai")
            if v is not None and isinstance(v, (int, float)):
                numeric_vals.append(float(v))
            else:
                null_count += 1

        stats = compute_statistics(numeric_vals)
        total_rows = len(decoded_rows)
        null_pct = round((null_count / total_rows * 100), 2) if total_rows > 0 else 0.0

        var_label = decoded_rows[0].get("variabel", f"Variabel {var_id}") if decoded_rows else f"Variabel {var_id}"
        var_unit = decoded_rows[0].get("satuan", "") if decoded_rows else ""

        summary_payload = {
            "ok": True,
            "protocol": PROTOCOL_VERSION,
            "bundle_id": f"bndl_{bundle_hash}",
            "var_id": var_id,
            "th_id": th_id,
            "domain": dom,
            "title": var_label,
            "unit": var_unit,
            "shape": {"rows": total_rows, "columns": len(decoded_rows[0]) if decoded_rows else 0},
            "null_count": null_count,
            "null_percentage": null_pct,
            "summary_statistics": stats,
            "head_rows": decoded_rows[:5],
            "tail_rows": decoded_rows[-5:] if total_rows > 5 else [],
            "_cached": False,
        }

        # Write preview bundle to disk
        bundle_dir.mkdir(parents=True, exist_ok=True)
        artifacts_dir = bundle_dir / "artifacts"
        artifacts_dir.mkdir(exist_ok=True)

        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary_payload, f, indent=2, ensure_ascii=False)

        manifest = {
            "protocol_version": PROTOCOL_VERSION,
            "bundle_id": f"bndl_{bundle_hash}",
            "software": "bps-web-api",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "ok",
            "cache_key": f"sha256:{bundle_hash}",
            "artifacts": ["summary.json", "artifacts/sample.csv"],
        }
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        # Write sample.csv
        sample_csv_path = artifacts_dir / "sample.csv"
        if decoded_rows:
            keys = list(decoded_rows[0].keys())
            with open(sample_csv_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(decoded_rows[:20])

        summary_payload["_bundle_dir"] = str(bundle_dir)
        return summary_payload
