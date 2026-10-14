#!/usr/bin/env python3
"""
BPS (Badan Pusat Statistik) Web API Client & CLI Tool
----------------------------------------------------
Authoritative, verified client designed for AI Agents and automated data pipelines.
Handles authentication, versioning (v1/v2), URL path formatting, error handling,
two-element pagination unwrapping, dynamic data key decoding, network retries,
and multi-format exporting (table, JSON, CSV).
"""

import os
import sys
import csv
import time
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, List, Optional, Tuple, Union


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
    """Parse key=value pairs from .env file into environment variables."""
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


# Initialize environment on import
load_env()


class BPSClient:
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
            raise ValueError(
                "BPS API Key not found. Set BPS_API_KEY in .env or pass it explicitly."
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
        """
        Build URL according to BPS path segment conventions:
        https://webapi.bps.go.id/{version}/api/{action}/{param1}/{val1}/{param2}/{val2}/key/{key}/
        """
        url_parts = [self.base_url, self.version, "api", action]
        for param, val in segments:
            if val is not None and str(val).strip() != "":
                url_parts.append(str(param))
                url_parts.append(urllib.parse.quote(str(val), safe=""))

        # Key is always appended as path segment
        url_parts.append("key")
        url_parts.append(urllib.parse.quote(self.api_key, safe=""))

        url = "/".join(url_parts) + "/"

        if query_params:
            filtered_query = {k: v for k, v in query_params.items() if v is not None}
            if filtered_query:
                url += "?" + urllib.parse.urlencode(filtered_query)

        return url

    def _request(self, url: str) -> Dict[str, Any]:
        """Execute HTTP request with safe headers, retry backoff, and robust error handling."""
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
                # Do not retry 4xx errors (client errors / unauthorized)
                if 400 <= e.code < 500:
                    try:
                        err_json = json.loads(err_body)
                        msg = err_json.get("message", err_body)
                    except Exception:
                        msg = err_body
                    raise RuntimeError(f"HTTP {e.code} Error from BPS API: {msg} (URL: {url})")

                # Retry 5xx server errors
                last_error = RuntimeError(f"HTTP {e.code} Server Error: {err_body}")
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
            except Exception as e:
                last_error = RuntimeError(f"Network error communicating with BPS API: {e} (URL: {url})")
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
        else:
            raise last_error

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON returned by BPS API: {content[:300]}")

        # Handle BPS V1 Masqueraded Errors (HTTP 200 with status: Error)
        status = data.get("status")
        if status == "Error":
            message = data.get("message", "Unknown BPS error")
            raise RuntimeError(f"BPS API Error: {message}")

        return data

    @staticmethod
    def _unwrap_list_response(resp: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Unwrap the BPS list pattern:
        response['data'] = [
            {'page': 1, 'pages': 5, 'total': 50, ...}, # pagination
            [{'id': 1, ...}, ...] # records
        ]
        Handles empty data: "" case safely.
        """
        raw_data = resp.get("data")
        if not raw_data or not isinstance(raw_data, list):
            return {"page": 1, "pages": 0, "total": 0, "count": 0}, []

        pagination = raw_data[0] if len(raw_data) > 0 and isinstance(raw_data[0], dict) else {}
        items = raw_data[1] if len(raw_data) > 1 and isinstance(raw_data[1], list) else []
        return pagination, items

    # -------------------------------------------------------------
    # Domain APIs
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

    # -------------------------------------------------------------
    # Metadata & Navigation APIs
    # -------------------------------------------------------------
    def get_subcats(self, domain: Optional[str] = None, page: int = 1) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Get list of Subject Categories."""
        dom = domain or self.default_domain
        segments = [("model", "subcat"), ("domain", dom), ("page", page)]
        url = self._build_url("list", segments)
        resp = self._request(url)
        return self._unwrap_list_response(resp)

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
    # Dynamic Data API & Composite Key Decoding
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
            ("th", th_id),  # MANDATORY in BPS API
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

        # Extract dimension definitions
        var_list = raw_data_response.get("var", [])
        if not var_list and "data" in raw_data_response and isinstance(raw_data_response["data"], list):
            var_list = raw_data_response["data"]

        vervar_list = raw_data_response.get("vervar", [])
        turvar_list = raw_data_response.get("turvar", [])
        tahun_list = raw_data_response.get("tahun", [])
        turtahun_list = raw_data_response.get("turtahun", [])

        # Default fallbacks if empty
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

                    for th in tahun_list:
                        th_val_str = str(th.get("val", ""))
                        th_label = th.get("label", "")

                        for turth in turtahun_list:
                            turth_val_str = str(turth.get("val", ""))
                            turth_label = turth.get("label", "")

                            composite_key = f"{ver_val_str}{v_val_str}{tur_val_str}{th_val_str}{turth_val_str}"
                            if composite_key in datacontent:
                                flat_records.append({
                                    label_vervar: ver_label,
                                    "Variabel": v_label,
                                    "Turunan Variabel": tur_label,
                                    "Tahun": th_label,
                                    "Periode": turth_label,
                                    "Nilai": datacontent[composite_key],
                                    "Satuan": v_unit,
                                    "_composite_key": composite_key,
                                })

        if len(flat_records) < len(datacontent):
            matched_keys = {r["_composite_key"] for r in flat_records}
            for k, val in datacontent.items():
                if k not in matched_keys:
                    flat_records.append({
                        label_vervar: "Unmatched",
                        "Variabel": var_list[0].get("label", ""),
                        "Turunan Variabel": "-",
                        "Tahun": "-",
                        "Periode": "-",
                        "Nilai": val,
                        "Satuan": var_list[0].get("unit", ""),
                        "_composite_key": k,
                    })

        return flat_records

    # -------------------------------------------------------------
    # Static Table APIs
    # -------------------------------------------------------------
    def get_static_tables(
        self,
        domain: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        month: Optional[str] = None,
        year: Optional[int] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """List static tables."""
        dom = domain or self.default_domain
        segments = [("model", "statictable"), ("domain", dom)]
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

    def get_static_table_detail(self, table_id: int, domain: Optional[str] = None, lang: Optional[str] = None) -> Dict[str, Any]:
        """Get detail of a static table (HTML table & Excel link)."""
        dom = domain or self.default_domain
        language = lang or self.default_lang
        segments = [("model", "statictable"), ("lang", language), ("domain", dom), ("id", table_id)]
        url = self._build_url("view", segments)
        resp = self._request(url)
        return resp.get("data", {})

    # -------------------------------------------------------------
    # Publications APIs
    # -------------------------------------------------------------
    def get_publications(
        self,
        domain: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        month: Optional[str] = None,
        year: Optional[int] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """List publications."""
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

    def get_publication_detail(self, pub_id: str, domain: Optional[str] = None, lang: Optional[str] = None) -> Dict[str, Any]:
        """Get publication detail including PDF download link."""
        dom = domain or self.default_domain
        language = lang or self.default_lang
        segments = [("model", "publication"), ("lang", language), ("domain", dom), ("id", pub_id)]
        url = self._build_url("view", segments)
        resp = self._request(url)
        return resp.get("data", {})

    # -------------------------------------------------------------
    # Press Releases (BRS) APIs
    # -------------------------------------------------------------
    def get_press_releases(
        self,
        domain: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        month: Optional[str] = None,
        year: Optional[int] = None,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """List Press Releases (Berita Resmi Statistik)."""
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

    def get_press_release_detail(self, brs_id: int, domain: Optional[str] = None, lang: Optional[str] = None) -> Dict[str, Any]:
        """Get full press release text and download links."""
        dom = domain or self.default_domain
        language = lang or self.default_lang
        segments = [("model", "pressrelease"), ("lang", language), ("domain", dom), ("id", brs_id)]
        url = self._build_url("view", segments)
        resp = self._request(url)
        return resp.get("data", {})

    # -------------------------------------------------------------
    # Strategic Indicators API
    # -------------------------------------------------------------
    def get_indicators(self, domain: Optional[str] = None, page: int = 1) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Get strategic macroeconomic indicators."""
        dom = domain or self.default_domain
        segments = [("model", "indicators"), ("domain", dom), ("page", page)]
        url = self._build_url("list", segments)
        resp = self._request(url)
        return self._unwrap_list_response(resp)

    # -------------------------------------------------------------
    # Foreign Trade (Exim) API
    # -------------------------------------------------------------
    def get_exim(
        self,
        sumber: int,  # 1: Export, 2: Import
        periode: int,  # 1: Monthly, 2: Annually
        kodehs: str,   # e.g. "03" for fish, "27" for mineral fuels
        jenishs: int,  # 1: 2-digit, 2: full HS Code
        tahun: Union[int, str],
    ) -> List[Dict[str, Any]]:
        """
        Fetch Foreign Trade (Export/Import) by HS Code.
        Endpoint: /v1/api/dataexim/sumber/{sumber}/periode/{periode}/kodehs/{kodehs}/jenishs/{jenishs}/tahun/{tahun}/key/{key}/
        """
        segments = [
            ("sumber", sumber),
            ("periode", periode),
            ("kodehs", kodehs),
            ("jenishs", jenishs),
            ("tahun", tahun),
        ]
        url = self._build_url("dataexim", segments)
        resp = self._request(url)
        raw_data = resp.get("data", [])
        return raw_data if isinstance(raw_data, list) else []

    # -------------------------------------------------------------
    # Census (Sensus Interoperabilitas) APIs
    # -------------------------------------------------------------
    def get_sensus_events(self) -> List[Dict[str, Any]]:
        """Get list of Census events (SP2020, ST2023, SP2010, etc.). Code: 37."""
        segments = [("datasource", "sensus"), ("id", 37)]
        url = self._build_url("interoperabilitas", segments)
        resp = self._request(url)
        _, items = self._unwrap_list_response(resp)
        return items

    def get_sensus_topics(self, event_id: str = "sp2020") -> List[Dict[str, Any]]:
        """Get list of Census topics for an event. Code: 38."""
        segments = [("datasource", "sensus"), ("id", 38), ("kegiatan", event_id)]
        url = self._build_url("interoperabilitas", segments)
        resp = self._request(url)
        _, items = self._unwrap_list_response(resp)
        return items

    def get_sensus_variables(self, event_id: str, topic_id: int) -> List[Dict[str, Any]]:
        """Get list of Census variables for an event and topic. Code: 40."""
        segments = [
            ("datasource", "sensus"),
            ("id", 40),
            ("kegiatan", event_id),
            ("topik", topic_id),
        ]
        url = self._build_url("interoperabilitas", segments)
        resp = self._request(url)
        _, items = self._unwrap_list_response(resp)
        return items

    def get_sensus_data(self, event_id: str, wilayah_sensus: str, dataset_id: int) -> Dict[str, Any]:
        """Get Census dataset records. Code: 41."""
        segments = [
            ("datasource", "sensus"),
            ("id", 41),
            ("kegiatan", event_id),
            ("wilayah_sensus", wilayah_sensus),
            ("dataset", dataset_id),
        ]
        url = self._build_url("interoperabilitas", segments)
        resp = self._request(url)
        return resp.get("data", {})

    # -------------------------------------------------------------
    # News & Infographics APIs
    # -------------------------------------------------------------
    def get_news(
        self,
        domain: Optional[str] = None,
        keyword: Optional[str] = None,
        newscat: Optional[str] = None,
        page: int = 1,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """List BPS news."""
        dom = domain or self.default_domain
        segments = [("model", "news"), ("domain", dom)]
        if keyword:
            segments.append(("keyword", keyword))
        if newscat:
            segments.append(("newscat", newscat))
        segments.append(("page", page))
        url = self._build_url("list", segments)
        resp = self._request(url)
        return self._unwrap_list_response(resp)

    def get_news_detail(self, news_id: int, domain: Optional[str] = None, lang: Optional[str] = None) -> Dict[str, Any]:
        """Get detail of BPS news."""
        dom = domain or self.default_domain
        language = lang or self.default_lang
        segments = [("model", "news"), ("lang", language), ("domain", dom), ("id", news_id)]
        url = self._build_url("view", segments)
        resp = self._request(url)
        return resp.get("data", {})

    def get_infographics(self, domain: Optional[str] = None, page: int = 1) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """List BPS infographics."""
        dom = domain or self.default_domain
        segments = [("model", "infographic"), ("domain", dom), ("page", page)]
        url = self._build_url("list", segments)
        resp = self._request(url)
        return self._unwrap_list_response(resp)

    def download_file(self, url: str, target_path: str) -> str:
        """Download remote binary file (PDF, report, etc.) with safe headers."""
        headers = {
            "User-Agent": "BPS-Agent-Client/1.0",
            "Accept": "*/*",
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as resp:
            content = resp.read()

        target_dir = os.path.dirname(os.path.abspath(target_path))
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)
        with open(target_path, "wb") as f:
            f.write(content)
        return target_path


# -------------------------------------------------------------
# Formatting & Export Helpers
# -------------------------------------------------------------
def format_table(rows: List[Dict[str, Any]]) -> str:
    if not rows:
        return "No records found."
    headers = list(rows[0].keys())
    headers = [h for h in headers if not h.startswith("_")]

    col_widths = {h: len(h) for h in headers}
    for r in rows:
        for h in headers:
            val_str = str(r.get(h, ""))
            if len(val_str) > col_widths[h]:
                col_widths[h] = min(len(val_str), 50)

    header_line = " | ".join(h.ljust(col_widths[h]) for h in headers)
    separator = "-+-".join("-" * col_widths[h] for h in headers)

    out_lines = [header_line, separator]
    for r in rows:
        row_line = " | ".join(str(r.get(h, ""))[:50].ljust(col_widths[h]) for h in headers)
        out_lines.append(row_line)
    return "\n".join(out_lines)


def export_csv(rows: List[Dict[str, Any]]) -> str:
    if not rows:
        return ""
    import io
    output = io.StringIO()
    headers = [h for h in rows[0].keys() if not h.startswith("_")]
    writer = csv.DictWriter(output, fieldnames=headers, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def output_result(data: Any, fmt: str, output_path: Optional[str] = None):
    """Output formatted string to stdout or file."""
    if fmt == "json":
        text = json.dumps(data, indent=2, ensure_ascii=False)
    elif fmt == "csv":
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            text = export_csv(data)
        else:
            text = json.dumps(data, indent=2, ensure_ascii=False)
    else:  # table
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            text = format_table(data)
        else:
            text = json.dumps(data, indent=2, ensure_ascii=False)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Result exported successfully to: {output_path}")
    else:
        print(text)


def build_parent_parser():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--key", help="BPS API Key (defaults to BPS_API_KEY from .env)")
    p.add_argument("--domain", help="BPS 4-digit Domain ID (e.g. 0000 for Nasional, 3200 for Jabar)")
    p.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
    p.add_argument("--output", help="Save output to file (e.g. data.csv, output.json)")
    return p


def main():
    common_p = build_parent_parser()
    parser = argparse.ArgumentParser(
        description="BPS (Badan Pusat Statistik) API CLI Client for AI Agents and Developers.",
        parents=[common_p]
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # domain
    cmd_dom = subparsers.add_parser("domain", parents=[common_p], help="List BPS domains")
    cmd_dom.add_argument("--type", choices=["all", "prov", "kab", "kabbyprov"], default="prov")
    cmd_dom.add_argument("--prov", help="Province ID when using kabbyprov")

    # subject
    cmd_subj = subparsers.add_parser("subject", parents=[common_p], help="List subjects")
    cmd_subj.add_argument("--subcat", type=int, help="Filter by subcategory ID")
    cmd_subj.add_argument("--keyword", help="Search keyword")
    cmd_subj.add_argument("--page", type=int, default=1)

    # variable
    cmd_var = subparsers.add_parser("variable", parents=[common_p], help="List statistical variables")
    cmd_var.add_argument("--subject", type=int, help="Filter by subject ID")
    cmd_var.add_argument("--keyword", help="Filter by title keyword")
    cmd_var.add_argument("--page", type=int, default=1)

    # period (th)
    cmd_th = subparsers.add_parser("period", parents=[common_p], help="List available period IDs (th) for a variable")
    cmd_th.add_argument("--var", type=int, required=True, help="Variable ID")
    cmd_th.add_argument("--page", type=int, default=1)

    # dynamic-data
    cmd_dyn = subparsers.add_parser("dynamic-data", parents=[common_p], help="Fetch and decode dynamic statistical data")
    cmd_dyn.add_argument("--var", type=int, required=True, help="Variable ID")
    cmd_dyn.add_argument("--th", required=True, help="Period ID (e.g. 126 or range 125:126)")
    cmd_dyn.add_argument("--turvar", help="Derived variable ID")
    cmd_dyn.add_argument("--vervar", help="Vertical variable ID")
    cmd_dyn.add_argument("--turth", help="Derived period ID")
    cmd_dyn.add_argument("--raw", action="store_true", help="Output raw JSON response without decoding")

    # statictable
    cmd_st = subparsers.add_parser("statictable", parents=[common_p], help="List static tables")
    cmd_st.add_argument("--keyword", help="Search keyword")
    cmd_st.add_argument("--page", type=int, default=1)

    # statictable-detail
    cmd_std = subparsers.add_parser("statictable-detail", parents=[common_p], help="Get static table detail & Excel link")
    cmd_std.add_argument("--id", type=int, required=True, help="Table ID")

    # publication
    cmd_pub = subparsers.add_parser("publication", parents=[common_p], help="List publications")
    cmd_pub.add_argument("--keyword", help="Search keyword")
    cmd_pub.add_argument("--page", type=int, default=1)

    # publication-detail
    cmd_pubd = subparsers.add_parser("publication-detail", parents=[common_p], help="Get publication detail & PDF link")
    cmd_pubd.add_argument("--id", required=True, help="Publication ID")

    # pressrelease
    cmd_brs = subparsers.add_parser("pressrelease", parents=[common_p], help="List Press Releases (BRS)")
    cmd_brs.add_argument("--keyword", help="Search keyword")
    cmd_brs.add_argument("--page", type=int, default=1)

    # pressrelease-detail
    cmd_brsd = subparsers.add_parser("pressrelease-detail", parents=[common_p], help="Get Press Release detail & PDF link")
    cmd_brsd.add_argument("--id", type=int, required=True, help="BRS ID")

    # indicators
    cmd_ind = subparsers.add_parser("indicators", parents=[common_p], help="List Strategic Macroeconomic Indicators")
    cmd_ind.add_argument("--page", type=int, default=1)

    # exim
    cmd_exim = subparsers.add_parser("exim", parents=[common_p], help="Foreign Trade Data (Ekspor/Impor per Kode HS)")
    cmd_exim.add_argument("--sumber", type=int, choices=[1, 2], default=1, help="1: Ekspor, 2: Impor")
    cmd_exim.add_argument("--periode", type=int, choices=[1, 2], default=2, help="1: Bulanan, 2: Tahunan")
    cmd_exim.add_argument("--kodehs", required=True, help="HS Code (e.g. 03 for ikan, 27 for migas)")
    cmd_exim.add_argument("--jenishs", type=int, choices=[1, 2], default=1, help="1: 2-digit, 2: full HS Code")
    cmd_exim.add_argument("--tahun", required=True, help="Tahun data (e.g. 2023)")

    # sensus
    cmd_sen = subparsers.add_parser("sensus", parents=[common_p], help="Census Events and Data")
    cmd_sen.add_argument("--action", choices=["events", "topics", "variables"], default="events")
    cmd_sen.add_argument("--event", default="sp2020", help="Event ID (e.g. sp2020, st2023)")
    cmd_sen.add_argument("--topic", type=int, help="Topic ID for variables")

    # news
    cmd_news = subparsers.add_parser("news", parents=[common_p], help="List BPS news")
    cmd_news.add_argument("--keyword", help="Search keyword")
    cmd_news.add_argument("--page", type=int, default=1)

    # infographic
    cmd_info = subparsers.add_parser("infographic", parents=[common_p], help="List BPS infographics")
    cmd_info.add_argument("--page", type=int, default=1)

    # download
    cmd_dl = subparsers.add_parser("download", parents=[common_p], help="Download binary file (PDF, report, etc.)")
    cmd_dl.add_argument("--url", required=True, help="Download URL")
    cmd_dl.add_argument("--file", required=True, help="Target local file path (e.g. report.pdf)")

    args = parser.parse_args()

    client = BPSClient(api_key=args.key, default_domain=args.domain)

    try:
        if args.command == "domain":
            items = client.get_domains(domain_type=args.type, prov=args.prov)
            output_result(items, args.format, args.output)

        elif args.command == "subject":
            _, items = client.get_subjects(domain=args.domain, subcat=args.subcat, page=args.page)
            if args.keyword:
                kw = args.keyword.lower()
                items = [i for i in items if kw in i.get("title", "").lower()]
            output_result(items, args.format, args.output)

        elif args.command == "variable":
            _, items = client.get_variables(subject=args.subject, domain=args.domain, page=args.page)
            if args.keyword:
                kw = args.keyword.lower()
                items = [i for i in items if kw in i.get("title", "").lower()]
            output_result(items, args.format, args.output)

        elif args.command == "period":
            _, items = client.get_periods(var_id=args.var, domain=args.domain, page=args.page)
            output_result(items, args.format, args.output)

        elif args.command == "dynamic-data":
            raw = client.get_dynamic_data(
                var_id=args.var,
                th_id=args.th,
                domain=args.domain,
                turvar_id=args.turvar,
                vervar_id=args.vervar,
                turth_id=args.turth,
            )
            if args.raw:
                output_result(raw, "json", args.output)
            else:
                decoded = client.decode_dynamic_data(raw)
                output_result(decoded, args.format, args.output)

        elif args.command == "statictable":
            _, items = client.get_static_tables(domain=args.domain, keyword=args.keyword, page=args.page)
            output_result(items, args.format, args.output)

        elif args.command == "statictable-detail":
            detail = client.get_static_table_detail(table_id=args.id, domain=args.domain)
            output_result(detail, "json", args.output)

        elif args.command == "publication":
            _, items = client.get_publications(domain=args.domain, keyword=args.keyword, page=args.page)
            output_result(items, args.format, args.output)

        elif args.command == "publication-detail":
            detail = client.get_publication_detail(pub_id=args.id, domain=args.domain)
            output_result(detail, "json", args.output)

        elif args.command == "pressrelease":
            _, items = client.get_press_releases(domain=args.domain, keyword=args.keyword, page=args.page)
            output_result(items, args.format, args.output)

        elif args.command == "pressrelease-detail":
            detail = client.get_press_release_detail(brs_id=args.id, domain=args.domain)
            output_result(detail, "json", args.output)

        elif args.command == "indicators":
            _, items = client.get_indicators(domain=args.domain, page=args.page)
            output_result(items, args.format, args.output)

        elif args.command == "exim":
            items = client.get_exim(
                sumber=args.sumber,
                periode=args.periode,
                kodehs=args.kodehs,
                jenishs=args.jenishs,
                tahun=args.tahun,
            )
            output_result(items, args.format, args.output)

        elif args.command == "sensus":
            if args.action == "events":
                items = client.get_sensus_events()
            elif args.action == "topics":
                items = client.get_sensus_topics(event_id=args.event)
            elif args.action == "variables":
                if not args.topic:
                    raise ValueError("--topic is required when action is 'variables'")
                items = client.get_sensus_variables(event_id=args.event, topic_id=args.topic)
            output_result(items, args.format, args.output)

        elif args.command == "news":
            _, items = client.get_news(domain=args.domain, keyword=args.keyword, page=args.page)
            output_result(items, args.format, args.output)

        elif args.command == "infographic":
            _, items = client.get_infographics(domain=args.domain, page=args.page)
            output_result(items, args.format, args.output)

        elif args.command == "download":
            path = client.download_file(url=args.url, target_path=args.file)
            print(f"File downloaded successfully to: {path}")

    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
