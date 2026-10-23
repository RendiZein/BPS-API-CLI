"""
Audit and Data Availability Probe Engine for BPS Web API.
Performs automated topic discovery, time series coverage inspection,
statistical anomaly harmonization (e.g. Papua regional split), and research formulation.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .api import BPSClient
from .cache import BPSCache


def audit_topic(
    client: BPSClient,
    topic: str,
    domain_query: Optional[str] = None,
    cache: Optional[BPSCache] = None,
    max_subjects: int = 3,
    max_vars_per_subject: int = 4,
) -> Dict[str, Any]:
    """
    Perform multi-step research feasibility audit:
    1. Resolve domain name/ID
    2. Match statistical subjects
    3. Probe variable time depth & dimension coverage
    4. Harmonize BPS statistical anomalies (pemekaran wilayah, temporal alignment)
    5. Query related press releases (BRS)
    6. Formulate 2-3 research proposal options
    """
    cache = cache or BPSCache()

    # Step 1: Resolve Domain
    domain_id = "0000"
    domain_name = "Indonesia (Nasional)"
    domain_type = "nasional"

    if domain_query:
        resolved = cache.search_domain(domain_query)
        if resolved:
            domain_id = resolved["domain_id"]
            domain_name = resolved["domain_name"]
            domain_type = resolved.get("domain_type", "prov")
        else:
            domain_id = domain_query
            domain_name = f"Domain {domain_query}"

    # Step 2: Match Subjects
    kw = topic.lower().strip()
    matched_subjects = []

    # Try local cache first for instant speed
    cached_subs = cache.search_subjects(kw, domain_id)
    if cached_subs:
        matched_subjects = cached_subs[:max_subjects]
    else:
        # Fallback to live API call
        _, live_subs = client.get_subjects(domain=domain_id, page=1)
        for s in live_subs:
            title = str(s.get("title", "")).lower()
            if kw in title or any(token in title for token in kw.split()):
                matched_subjects.append(s)
                if len(matched_subjects) >= max_subjects:
                    break

    # If still empty, search national domain subjects
    if not matched_subjects and domain_id != "0000":
        _, nat_subs = client.get_subjects(domain="0000", page=1)
        for s in nat_subs:
            title = str(s.get("title", "")).lower()
            if kw in title or any(token in title for token in kw.split()):
                matched_subjects.append(s)
                if len(matched_subjects) >= max_subjects:
                    break

    # Step 3: Probe Variables & Time Depth
    subject_results = []
    total_vars_found = 0

    for sub in matched_subjects:
        sub_id = int(sub.get("sub_id", 0))
        sub_title = sub.get("title", "")

        _, vars_list = client.get_variables(subject=sub_id, domain=domain_id, page=1)
        total_vars_found += len(vars_list)

        probed_vars = []
        for v in vars_list[:max_vars_per_subject]:
            var_id = int(v.get("var_id", 0))
            var_title = v.get("title", "")
            var_unit = v.get("unit", "")

            # Probe period availability
            years_available = []
            try:
                _, periods = client.get_periods(var_id=var_id, domain=domain_id, page=1)
                for p in periods:
                    th_label = p.get("th") or p.get("tahun") or p.get("label")
                    if th_label:
                        years_available.append(str(th_label))
            except Exception:
                pass

            probed_vars.append({
                "var_id": var_id,
                "title": var_title,
                "unit": var_unit,
                "periods_count": len(years_available),
                "years_sample": years_available[:6],
                "time_span": f"{years_available[-1]} - {years_available[0]}" if len(years_available) >= 2 else (years_available[0] if years_available else "Unknown"),
            })

        subject_results.append({
            "subject_id": sub_id,
            "title": sub_title,
            "variables_found": len(vars_list),
            "probed_variables": probed_vars,
        })

    # Step 4: Detect Statistical Quirks & Anomalies
    anomalies = []
    # Check Papua provinces split in 2022
    papua_domains = {"9100", "9400", "9500", "9600", "9700"}
    if domain_id in papua_domains:
        anomalies.append(
            "Perhatian Metodologi Pemekaran Papua (2022): Terjadi pemekaran wilayah dari Papua & Papua Barat "
            "menjadi 4 DOB baru (Papua Selatan, Papua Tengah, Papua Pegunungan, Papua Barat Daya). "
            "Data panel rentang waktu 2018-2024 akan mengalami diskontinuitas wilayah."
        )

    # Check temporal alignment
    temporal_notes = "Variabel BPS memiliki siklus rilis bervariasi: Kemiskinan (Semesteran: Maret & September), Inflasi (Bulanan), PDRB (Triwulanan & Tahunan), IPM (Tahunan)."

    # Step 5: Query Related BRS / Publications
    related_brs = []
    try:
        _, brs_items = client.get_press_releases(domain=domain_id, keyword=topic, page=1)
        for b in brs_items[:3]:
            related_brs.append({
                "brs_id": b.get("brs_id"),
                "title": b.get("title"),
                "release_date": b.get("rl_date"),
            })
    except Exception:
        pass

    # Step 6: Formulate Research Options
    research_proposals = []
    if subject_results and any(s["probed_variables"] for s in subject_results):
        research_proposals = [
            {
                "option": "A",
                "title": "Analisis Tren & Evaluasi Kebijakan (Time Series)",
                "description": f"Memetakan evolusi indikator {topic} dalam rentang waktu historis pada wilayah {domain_name}.",
                "feasibility": "HIGH" if any(len(v.get("years_sample", [])) >= 3 for s in subject_results for v in s["probed_variables"]) else "MEDIUM",
            },
            {
                "option": "B",
                "title": "Analisis Komparasi Spasial Antar-Wilayah",
                "description": f"Membandingkan disparitas capaian {topic} antar-kabupaten/kota di bawah {domain_name}.",
                "feasibility": "HIGH" if domain_type in {"prov", "nasional"} else "LOW",
            },
            {
                "option": "C",
                "title": "Regresi Data Panel Ekonometrika",
                "description": f"Menggabungkan observasi temporal dan cross-section wilayah untuk estimasi dampak kebijakan.",
                "feasibility": "MEDIUM",
            },
        ]

    return {
        "ok": True,
        "topic": topic,
        "domain": {
            "id": domain_id,
            "name": domain_name,
            "type": domain_type,
        },
        "subjects_matched_count": len(subject_results),
        "total_variables_discovered": total_vars_found,
        "subjects": subject_results,
        "data_anomalies": anomalies,
        "temporal_alignment_notes": temporal_notes,
        "related_brs": related_brs,
        "research_proposals": research_proposals,
    }


def inspect_variable(client: BPSClient, var_id: int, domain: Optional[str] = None) -> Dict[str, Any]:
    """In-depth inspection of a specific variable dimensions and period IDs."""
    domain_id = domain or client.default_domain

    # 1. Available periods
    _, periods = client.get_periods(var_id=var_id, domain=domain_id, page=1)

    # 2. Derived variables (turvar)
    try:
        turvar_items = client.get_derived_variables(var_id=var_id, domain=domain_id)
    except Exception:
        turvar_items = []

    # 3. Vertical categories (vervar)
    try:
        vervar_items = client.get_vertical_variables(var_id=var_id, domain=domain_id)
    except Exception:
        vervar_items = []

    return {
        "ok": True,
        "var_id": var_id,
        "domain": domain_id,
        "periods_available": periods,
        "periods_count": len(periods),
        "derived_classifications_turvar": turvar_items,
        "vertical_categories_vervar": vervar_items,
    }
