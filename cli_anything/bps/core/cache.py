"""
Local SQLite Caching for BPS Metadata (Domains & Subjects).
Enables instant (<5ms) offline topic discovery, domain name resolution, and reduces BPS API hits.
Cross-platform safe (explicit connection closure for Windows file lock release).
"""

from __future__ import annotations

import contextlib
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_CACHE_DB = Path(".bps_cache.db")


class BPSCache:
    """Local SQLite cache for static/semi-static BPS metadata."""

    def __init__(self, db_path: Optional[str | Path] = None):
        self.db_path = Path(db_path) if db_path else DEFAULT_CACHE_DB
        self._init_db()

    @contextlib.contextmanager
    def _connect(self):
        """Context manager guaranteeing connection closure to prevent Windows file-lock errors."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        """Create tables if not existing."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS domains (
                    domain_id TEXT PRIMARY KEY,
                    domain_name TEXT NOT NULL,
                    domain_type TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subjects (
                    sub_id INTEGER,
                    domain_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    subcat_id INTEGER,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (sub_id, domain_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cache_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def sync_domains(self, domains_list: List[Dict[str, Any]]) -> int:
        """Upsert domains list into cache."""
        now = datetime.now(timezone.utc).isoformat()
        count = 0
        with self._connect() as conn:
            cursor = conn.cursor()
            for d in domains_list:
                domain_id = str(d.get("domain_id") or d.get("id") or "")
                domain_name = str(d.get("domain_name") or d.get("name") or "")
                domain_type = str(d.get("domain_type") or d.get("type") or "all")
                if domain_id:
                    cursor.execute("""
                        INSERT OR REPLACE INTO domains (domain_id, domain_name, domain_type, updated_at)
                        VALUES (?, ?, ?, ?)
                    """, (domain_id, domain_name, domain_type, now))
                    count += 1
            cursor.execute("""
                INSERT OR REPLACE INTO cache_meta (key, value, updated_at)
                VALUES ('domains_last_sync', ?, ?)
            """, (str(count), now))
            conn.commit()
        return count

    def sync_subjects(self, domain_id: str, subjects_list: List[Dict[str, Any]]) -> int:
        """Upsert subjects list for a domain into cache."""
        now = datetime.now(timezone.utc).isoformat()
        count = 0
        with self._connect() as conn:
            cursor = conn.cursor()
            for s in subjects_list:
                sub_id = s.get("sub_id")
                title = s.get("title") or s.get("name") or ""
                subcat_id = s.get("subcat_id")
                if sub_id:
                    cursor.execute("""
                        INSERT OR REPLACE INTO subjects (sub_id, domain_id, title, subcat_id, updated_at)
                        VALUES (?, ?, ?, ?, ?)
                    """, (int(sub_id), str(domain_id), str(title), subcat_id, now))
                    count += 1
            conn.commit()
        return count

    def search_domain(self, query: str) -> Optional[Dict[str, str]]:
        """Search domain by ID or fuzzy name match (e.g. 'Jawa Timur', 'Jatim', 'Surabaya', '3500')."""
        q = query.strip()
        with self._connect() as conn:
            cursor = conn.cursor()
            # 1. Exact ID match
            cursor.execute("SELECT domain_id, domain_name, domain_type FROM domains WHERE domain_id = ?", (q,))
            row = cursor.fetchone()
            if row:
                return dict(row)

            # 2. Case-insensitive exact name match
            cursor.execute("SELECT domain_id, domain_name, domain_type FROM domains WHERE LOWER(domain_name) = LOWER(?)", (q,))
            row = cursor.fetchone()
            if row:
                return dict(row)

            # 3. Partial substring match
            cursor.execute("SELECT domain_id, domain_name, domain_type FROM domains WHERE domain_name LIKE ? ORDER BY domain_id ASC LIMIT 1", (f"%{q}%",))
            row = cursor.fetchone()
            if row:
                return dict(row)

        # Fallback dictionary for common Indonesian nicknames if cache not yet populated
        nicknames = {
            "nasional": ("0000", "Indonesia"),
            "indonesia": ("0000", "Indonesia"),
            "jatim": ("3500", "Provinsi Jawa Timur"),
            "jawa timur": ("3500", "Provinsi Jawa Timur"),
            "jateng": ("3300", "Provinsi Jawa Tengah"),
            "jawa tengah": ("3300", "Provinsi Jawa Tengah"),
            "jabar": ("3200", "Provinsi Jawa Barat"),
            "jawa barat": ("3200", "Provinsi Jawa Barat"),
            "dki": ("3100", "DKI Jakarta"),
            "jakarta": ("3100", "DKI Jakarta"),
            "diy": ("3400", "DI Yogyakarta"),
            "jogja": ("3400", "DI Yogyakarta"),
            "yogyakarta": ("3400", "DI Yogyakarta"),
            "banten": ("3600", "Provinsi Banten"),
            "bali": ("5100", "Provinsi Bali"),
            "sumut": ("1200", "Provinsi Sumatera Utara"),
            "sumatera utara": ("1200", "Provinsi Sumatera Utara"),
            "sumsel": ("1600", "Provinsi Sumatera Selatan"),
            "sumatera selatan": ("1600", "Provinsi Sumatera Selatan"),
        }
        clean_q = q.lower().strip()
        if clean_q in nicknames:
            d_id, d_name = nicknames[clean_q]
            return {"domain_id": d_id, "domain_name": d_name, "domain_type": "prov"}

        return None

    def search_subjects(self, keyword: str, domain_id: str = "0000") -> List[Dict[str, Any]]:
        """Search subjects using instant SQLite LIKE query."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT sub_id, domain_id, title, subcat_id
                FROM subjects
                WHERE (domain_id = ? OR domain_id = '0000') AND title LIKE ?
                ORDER BY sub_id ASC
            """, (domain_id, f"%{keyword}%"))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def status(self) -> Dict[str, Any]:
        """Get cache statistics and size."""
        if not self.db_path.exists():
            return {"status": "UNINITIALIZED", "domains_count": 0, "subjects_count": 0}

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM domains")
            domains_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM subjects")
            subjects_count = cursor.fetchone()[0]
            cursor.execute("SELECT value, updated_at FROM cache_meta WHERE key = 'domains_last_sync'")
            meta = cursor.fetchone()

        return {
            "status": "READY" if domains_count > 0 else "EMPTY",
            "db_path": str(self.db_path),
            "domains_count": domains_count,
            "subjects_count": subjects_count,
            "last_synced": meta["updated_at"] if meta else None,
        }

    def clear(self) -> None:
        """Clear cache tables."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM domains")
            cursor.execute("DELETE FROM subjects")
            cursor.execute("DELETE FROM cache_meta")
            conn.commit()
