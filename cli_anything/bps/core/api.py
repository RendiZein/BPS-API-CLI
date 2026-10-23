"""
Core HTTP client and composite key decoder for BPS Web API.
Zero external dependencies (pure Python standard library).
Handles WAF backoff, composite key unwrapping, and endpoint normalization.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple, Union

from ..utils.error_handler import BPSAuthError, BPSError, BPSNotFoundError, BPSRateLimitError


def find_env_file() -> Optional[str]:
    """Search for .env file starting from current directory upwards."""
    curr = os.path.abspath(os.getcwd())
    while True:
        candidate = os.path.join(curr, ".env")
        if os.path.exists(candidate):
            return candidate
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return None


def load_env(env_path: Optional[str] = None) -> Dict[str, str]:
    """Parse key=value pairs from .env file into os.environ."""
    path = env_path or find_env_file()
    env_vars = {}
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    env_vars[k] = v
                    if k not in os.environ:
                        os.environ[k] = v
    return env_vars


# Auto-load on import
load_env()


class BPSClient:
    """Production client for BPS Web API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        version: Optional[str] = None,
        base_url: Optional[str] = None,
        default_domain: Optional[str] = None,
        default_lang: Optional[str] = None,
        timeout: int = 25,
        max_retries: int = 3,
    ):
        self.api_key = (
            api_key
            or os.environ.get("BPS_API_KEY")
            or os.environ.get("key_api_bps")
        )
        if not self.api_key:
            raise BPSAuthError(
                "BPS API Key not found. Please set BPS_API_KEY in your .env file or environment."
            )

        self.version = (version or os.environ.get("BPS_API_VERSION", "v1")).lower()
        self.base_url = (
            base_url or os.environ.get("BPS_API_BASE_URL", "https://webapi.bps.go.id")
        ).rstrip("/")
        self.default_domain = default_domain or os.environ.get("BPS_DEFAULT_DOMAIN", "0000")
        self.default_lang = default_lang or os.environ.get("BPS_DEFAULT_LANG", "ind")
        self.timeout = timeout or int(os.environ.get("BPS_TIMEOUT", "25"))
        self.max_retries = max_retries

    def _build_url(
        self,
        action: str,
        segments: List[Tuple[str, Any]],
        query_params: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build URL formatted as: {base_url}/{version}/api/{action}/{param1}/{val1}/.../key/{key}/"""
        url_parts = [self.base_url, self.version, "api", action]
        for param, val in segments:
            if val is not None and str(val).strip() != "":
                url_parts.append(str(param))
                url_parts.append(urllib.parse.quote(str(val), safe=""))

        url_parts.append("key")
        url_parts.append(urllib.parse.quote(self.api_key, safe=""))

        url = "/".join(url_parts) + "/"

        if query_params:
            filtered_query = {k: v for k, v in query_params.items() if v is not None}
            if filtered_query:
                url += "?" + urllib.parse.urlencode(filtered_query)

        return url

    def _request(self, url: str) -> Dict[str, Any]:
        """Execute HTTP request with safe headers, retry backoff, and WAF detection."""
        headers = {
            "User-Agent": "BPS-Agent-Client/1.0",
            "Accept": "*/*",
        }
        req = urllib.request.Request(url, headers=headers)

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    content = response.read().decode("utf-8")
                break
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="ignore")
                if e.code == 403:
                    raise BPSRateLimitError(
                        f"HTTP 403 Perimeter block or rate limit triggered: {err_body}"
                    )
                if 400 <= e.code < 500:
                    try:
                        err_json = json.loads(err_body)
                        msg = err_json.get("message", err_body)
                    except Exception:
                        msg = err_body
                    raise BPSError(f"HTTP {e.code} Error from BPS API: {msg}")

                last_error = BPSError(f"HTTP {e.code} Server Error from BPS API: {err_body}")
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
            except Exception as e:
                last_error = BPSError(f"Network error communicating with BPS API: {e}")
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
        else:
            raise last_error or BPSError("Failed to contact BPS API after maximum retries.")

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            raise BPSError(f"Invalid JSON returned by BPS API: {content[:300]}")

        status = data.get("status")
        if status == "Error":
            message = data.get("message", "Unknown BPS error")
            raise BPSError(f"BPS API Error: {message}")

        return data

    @staticmethod
    def _unwrap_list_response(resp: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Unwrap the BPS list pattern [pagination_dict, items_list]."""
        raw_data = resp.get("data")
        if not raw_data or not isinstance(raw_data, list):
            return {"page": 1, "pages": 0, "total": 0, "count": 0}, []

        pagination = raw_data[0] if len(raw_data) > 0 and isinstance(raw_data[0], dict) else {}
        items = raw_data[1] if len(raw_data) > 1 and isinstance(raw_data[1], list) else []
        return pagination, items

    # -------------------------------------------------------------
    # Domain & Navigation APIs
    # -------------------------------------------------------------
    def get_domains(self, domain_type: str = "all", prov: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get BPS domains (type: 'all', 'prov', 'kab', or 'kabbyprov')."""
        segments = [("type", domain_type)]
        if domain_type == "kabbyprov":
            if not prov:
                raise ValueError("Parameter 'prov' is required when domain_type is 'kabbyprov'")
            segments.append(("prov", prov))
        url = self._build_url("domain", segments)
        resp = self._request(url)
        _, items = self._unwrap_list_response(resp)
        return items

    def get_subjects(
        self,
        domain: Optional[str] = None,
        subcat: Optional[int] = None,
        page: int = 1,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Get list of Subjects (Topik Statistik)."""
        dom = domain or self.default_domain
        segments = [("model", "subject"), ("domain", dom)]
        if subcat:
            segments.append(("subcat", subcat))
        segments.append(("page", page))
        url = self._build_url("list", segments)
        resp = self._request(url)
        return self._unwrap_list_response(resp)

    def get_variables(
        self,
        subject: Optional[int] = None,
        domain: Optional[str] = None,
        page: int = 1,
        year: Optional[int] = None,
        area: Optional[int] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Get list of statistical variables."""
        dom = domain or self.default_domain
        segments = [("model", "var"), ("domain", dom)]
        if subject:
            segments.append(("subject", subject))
        if year:
            segments.append(("year", year))
        if area is not None:
            segments.append(("area", area))
        segments.append(("page", page))
        url = self._build_url("list", segments)
        resp = self._request(url)
        return self._unwrap_list_response(resp)

    def get_periods(self, var_id: int, domain: Optional[str] = None, page: int = 1) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Get available period IDs ('th') for a specific variable."""
        dom = domain or self.default_domain
        segments = [("model", "th"), ("domain", dom), ("var", var_id), ("page", page)]
        url = self._build_url("list", segments)
        resp = self._request(url)
        return self._unwrap_list_response(resp)

    def get_derived_variables(self, var_id: int, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get derived variables ('turvar') for a variable."""
        dom = domain or self.default_domain
        segments = [("model", "turvar"), ("domain", dom), ("var", var_id)]
        url = self._build_url("list", segments)
        resp = self._request(url)
        _, items = self._unwrap_list_response(resp)
        return items

    def get_vertical_variables(self, var_id: int, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get vertical variables ('vervar') for a variable."""
        dom = domain or self.default_domain
        segments = [("model", "vervar"), ("domain", dom), ("var", var_id)]
        url = self._build_url("list", segments)
        resp = self._request(url)
        _, items = self._unwrap_list_response(resp)
        return items

    # -------------------------------------------------------------
    # Dynamic Data & Composite Key Decoding
    # -------------------------------------------------------------
    def get_dynamic_data(
        self,
        var_id: int,
        th_id: Union[int, str],
        domain: Optional[str] = None,
        turvar_id: Optional[Union[int, str]] = None,
        vervar_id: Optional[Union[int, str]] = None,
        turth_id: Optional[Union[int, str]] = None,
    ) -> Dict[str, Any]:
        """Fetch raw dynamic data matrix."""
        dom = domain or self.default_domain
        segments = [
            ("model", "data"),
            ("domain", dom),
            ("var", var_id),
            ("th", th_id),
        ]
        if turvar_id is not None:
            segments.append(("turvar", turvar_id))
        if vervar_id is not None:
            segments.append(("vervar", vervar_id))
        if turth_id is not None:
            segments.append(("turth", turth_id))

        url = self._build_url("list", segments)
        return self._request(url)

    def decode_dynamic_data(self, raw_data_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Decode BPS composite keys in 'datacontent' to clean flat tabular records.
        Key structure: {vervar_val}{var_val}{turvar_val}{tahun_val}{turtahun_val}
        """
        datacontent = raw_data_response.get("datacontent", {})
        if not datacontent or not isinstance(datacontent, dict):
            return []

        var_list = raw_data_response.get("var", [])
        if not var_list and "data" in raw_data_response and isinstance(raw_data_response["data"], list):
            var_list = raw_data_response["data"]

        vervar_list = raw_data_response.get("vervar", [])
        turvar_list = raw_data_response.get("turvar", [])
        tahun_list = raw_data_response.get("tahun", [])
        turtahun_list = raw_data_response.get("turtahun", [])

        if not var_list:
            var_list = [{"val": "", "label": "Unknown Variable", "unit": ""}]
        if not vervar_list:
            vervar_list = [{"val": "0", "label": "Total"}]
        if not turvar_list:
            turvar_list = [{"val": "0", "label": "None"}]
        if not tahun_list:
            tahun_list = [{"val": "0", "label": "None"}]
        if not turtahun_list:
            turtahun_list = [{"val": "0", "label": "None"}]

        label_vervar = raw_data_response.get("labelvervar", "Kategori Vertikal")

        flat_records = []
        for v in var_list:
            v_val_str = str(v.get("val", ""))
            v_label = v.get("label", "")
            v_unit = v.get("unit", "")

            for ver in vervar_list:
                ver_val_str = str(ver.get("val", ""))
                ver_label = ver.get("label", "")

                for tur in turvar_list:
                    tur_val_str = str(tur.get("val", ""))
                    tur_label = tur.get("label", "")

                    for thn in tahun_list:
                        thn_val_str = str(thn.get("val", ""))
                        thn_label = thn.get("label", "")

                        for tthn in turtahun_list:
                            tthn_val_str = str(tthn.get("val", ""))
                            tthn_label = tthn.get("label", "")

                            composite_key = f"{ver_val_str}{v_val_str}{tur_val_str}{thn_val_str}{tthn_val_str}"

                            if composite_key in datacontent:
                                raw_val = datacontent[composite_key]
                                num_val = None
                                if raw_val is not None:
                                    try:
                                        num_val = float(raw_val)
                                    except ValueError:
                                        num_val = raw_val

                                record = {
                                    "variabel_id": v_val_str,
                                    "variabel": v_label,
                                    "satuan": v_unit,
                                    "kategori_vertikal": ver_label,
                                    "kategori_turunan": tur_label,
                                    "tahun": thn_label,
                                    "periode": tthn_label,
                                    "nilai": num_val,
                                    "composite_key": composite_key,
                                }
                                flat_records.append(record)

        return flat_records

    # -------------------------------------------------------------
    # Strategic Indicators & Publications
    # -------------------------------------------------------------
    def get_indicators(self, domain: Optional[str] = None, page: int = 1) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Fetch Strategic Economic Indicators (PDRB, Inflasi, Kemiskinan, Pengangguran)."""
        dom = domain or self.default_domain
        segments = [("model", "indicators"), ("domain", dom), ("page", page)]
        url = self._build_url("list", segments)
        resp = self._request(url)
        return self._unwrap_list_response(resp)

    def get_publications(
        self,
        domain: Optional[str] = None,
        keyword: Optional[str] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
        page: int = 1,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Search publications."""
        dom = domain or self.default_domain
        segments = [("model", "publication"), ("domain", dom)]
        if keyword:
            segments.append(("keyword", keyword))
        if month:
            segments.append(("month", month))
        if year:
            segments.append(("year", year))
        segments.append(("page", page))
        url = self._build_url("list", segments)
        resp = self._request(url)
        return self._unwrap_list_response(resp)

    def get_press_releases(
        self,
        domain: Optional[str] = None,
        keyword: Optional[str] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
        page: int = 1,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Search Berita Resmi Statistik (BRS)."""
        dom = domain or self.default_domain
        segments = [("model", "pressrelease"), ("domain", dom)]
        if keyword:
            segments.append(("keyword", keyword))
        if month:
            segments.append(("month", month))
        if year:
            segments.append(("year", year))
        segments.append(("page", page))
        url = self._build_url("list", segments)
        resp = self._request(url)
        return self._unwrap_list_response(resp)
