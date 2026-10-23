# GRAND PLAN: BPS API Agent-Native CLI Suite & Antigravity Skill
> **Metodologi Arsitektur**: Standar 100% Penuh **HKUDS/CLI-Anything** (*Agent-Native Harness, SHA-256 Preview Protocol, Trajectory, Windows Pipe Resilience, AST Skill Generator, Coverage Matrix & Harness Validator*) dipadukan dengan **Domain Intelligence Riset BPS RI**  
> **Target Pengguna**: Antigravity AI Agent & Peneliti / Data Analyst (Human-in-the-loop)  
> **Status**: Dokumen Spesifikasi Induk Final (Definitive Production Specification)

---

## 1. Executive Summary & Visi Proyek

Proyek ini mentransformasikan **`sbps_api_skill`** menjadi sebuah **Agent-Native Statistical Research Suite** berstandar industri untuk Badan Pusat Statistik (BPS) Republik Indonesia.

Bukan sekadar *data fetcher* mekanis, sistem ini bertindak sebagai **Autonomous Research Partner & Data Auditor** bagi pengguna Antigravity yang mampu:
1. Memeriksa kesiapan dan latensi server API BPS secara preventif (`bps status`).
2. Melakukan audit topik riset secara instan via *Local Cache* tanpa menghabiskan kuota harian.
3. Menyelaraskan anomali statistik BPS (pemekaran wilayah Papua 34 $\rightarrow$ 38 provinsi, perbedaan frekuensi waktu bulanan vs semesteran).
4. Menyajikan proposal riset yang terbukti memiliki data pendukung (*evidence-based*).
5. Menghasilkan *preview bundle* dengan *SHA-256 fingerprint caching* yang hemat token.
6. Mengeksekusi penarikan data yang aman dari pemblokiran WAF, lengkap dengan ringkasan metadata (*codebook*) dan visualisasi awal.
7. Menjaga sinkronisasi dokumentasi AI secara otomatis menggunakan generator AST Python (`skill_generator.py`).

```
┌─────────────────────────────────────────────────────────────┐
│                       USER PROMPT                           │
│  "Analisis dampak inflasi terhadap kemiskinan di Jatim"     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   ANTIGRAVITY AI AGENT                      │
│     (Membaca SKILL.md & mengeksekusi binary global `bps`)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│   FASE 0: READINESS & HEALTH PROBE                          │
│   • bps status --json (Cek API key valid & server online)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│   FASE 1: SESSION INIT & PROBE AUDIT (LOCAL + API)          │
│   • bps session init --domain 3500 --name "Jatim_Riset"     │
│   • bps audit --topic "kemiskinan" --json                   │
│   • bps audit --topic "inflasi" --json                      │
│   ──> Output: Matriks tahun tersedia, level wilayah, BRS    │
│   ──> State: Tercatat otomatis di `trajectory.json`         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│   FASE 2: RESEARCH FORMULATION & FEASIBILITY                │
│   • AI mengevaluasi keselarasan frekuensi (bulan vs semester)│
│   • AI merumuskan 2-3 opsi analisis realistis               │
│   • User memilih proposal yang diinginkan                   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│   FASE 3: CONTENT-ADDRESSABLE PREVIEW (SHA-256 Cache)       │
│   • bps preview --var 123 --th 126 --json                   │
│   ──> Output: `summary.json` (shape, null %, mean, min, max)│
│       dan sampel tanpa membanjiri konteks LLM               │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│   FASE 4: DRY-RUN SAFETY CHECK & EXPORT                     │
│   • bps fetch --var 123 --format csv --dry-run              │
│   • bps fetch --var 123 --format csv --output data/hasil.csv│
│   • AI memverifikasi keberadaan file fisik di disk          │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Enam Belas Pilar Arsitektur Terintegrasi (100% HKUDS Standard)

Seluruh prinsip rekayasa dari riset **HKUDS/CLI-Anything** (`HARNESS.md`, `PREVIEW_PROTOCOL.md`, `validate.md`, `session-locking.md`, `skill_generator.py`, `preview_bundle.py`, `refine.md`) dipadukan secara utuh dengan **Kebutuhan Substantif Riset BPS**:

| # | Pilar Arsitektur | Spesifikasi Teknis | Dampak Operasional |
| :--- | :--- | :--- | :--- |
| **1** | **Global Executable (PEP 420)** | Namespace package `cli_anything.bps` didaftarkan lewat `setup.py` dengan entry point `bps` dan `cli-anything-bps`. | Agen memanggil `bps audit ...` dari direktori mana pun tanpa path relatif panjang atau ketergantungan `cwd`. |
| **2** | **Readiness & Health Probe** | Perintah `bps status` / `bps ping` mengecek validitas API Key, latensi jaringan, dan status server BPS. | Mencegah AI mengalami *timeout* atau gagal di tengah alur jika server BPS sedang *maintenance (503)*. |
| **3** | **Probe Before Action** | Perintah `bps audit` & `bps inspect` wajib dijalankan sebelum data ditarik. | Mencegah AI halusinasi atau mengunduh dataset kosong. |
| **4** | **3-Layer Preview Protocol** | Emisi folder `preview-bundle/v1` berisi `manifest.json`, `summary.json`, dan direktori `artifacts/`. | Agen mengonsumsi `summary.json` (statistik, missing %) tanpa memuat ribuan baris CSV ke dalam *context window*. |
| **5** | **Content-Addressable SHA-256 Preview Cache** | Hash sidik jari `fingerprint_data({"var": ..., "th": ..., "domain": ...})`. | Jika data dengan parameter yang sama pernah ditarik, preview disajikan seketika (<5ms) tanpa request ulang ke API BPS. |
| **6** | **Snapshot Session & Undo/Redo** | Stack history sesi hingga 50 level dengan *cross-platform atomic file locking* (`msvcrt` di Windows, `fcntl` di POSIX) pada `.bps_session.json`. | Agen dapat melakukan `bps session undo` jika salah memilih variabel tanpa merusak state sesi di Windows maupun Linux. |
| **7** | **Permanent Replay Trajectory** | File log append-only `trajectory.json` mendampingi setiap sesi. | Mencatat setiap *step ID*, perintah, timestamp, dan ID bundle preview untuk transparansi rekam jejak riset (*data provenance*). |
| **8** | **Pemisahan Aliran `stdout` & `stderr`** | `@handle_error` decorator: `stdout` **khusus** untuk JSON murni data, `stderr` untuk log/progress/error. | AI dapat mem-parse JSON dari `stdout` dengan 100% deterministik tanpa tercampur pesan log. Return code: `0` (sukses), non-zero (gagal). |
| **9** | **Resiliensi Windows & Piped REPL** | Deteksi `_supports_interactive_prompt()` (`sys.stdin.isatty() and sys.stdout.isatty()`). | Mencegah `NoConsoleScreenBufferError` di Windows PowerShell saat pengujian piping (`\|`), dengan *fallback* aman ke input ASCII murni. |
| **10** | **AST Automated SKILL.md Sync** | Parser AST Python (`skill_generator.py`) yang mengekstrak perintah Click, docstring, dan opsi untuk menghasilkan `SKILL.md`. | Dokumentasi AI selalu 100% sinkron dengan kode tanpa risiko lupa update manual. |
| **11** | **Traceability Contract (`coverage.matrix.json`)** | Pemetaan deklaratif antara *Use Case*, Perintah CLI, Endpoint BPS, Unit Test, dan E2E Test. | Jaminan audit bahwa 100% endpoint BPS dan alur riset memiliki cakupan tes otomatis yang terverifikasi. |
| **12** | **Spesifikasi Domain: `BPS.md`** | Dokumen arsitektur lengkap berisi batasan rute V1/V2, parameter wajib (`th`, `lang`), dan formula dekoder matriks komposit `datacontent`. | Menjadi *single source of truth* teknis bagi pengembang dan agen AI. |
| **13** | **Automated Harness Validator (`verify_harness.py`)** | Skrip linter otomatis yang memvalidasi struktur plugin, skema JSON, opsi `--json`, dan kepatuhan HARNESS.md. | Memastikan standar kualitas tetap terjaga sebelum plugin dirilis. |
| **14** | **Safety Guard: `--dry-run` & Rate-Limit** | Flag `--dry-run` pada seluruh operasi mutasi dan fetch data. | Menghitung jumlah panggilan HTTP dan estimasi jeda *backoff* sebelum menembak server BPS, mencegah pemblokiran WAF. |
| **15** | **Local Cache & Harmonisasi Statistik** | Penyimpanan lokal SQLite untuk katalog Domain/Subjek + modul anomali pemekaran Papua (34 $\rightarrow$ 38) dan harmonisasi frekuensi. | Audit instan (<100ms) tanpa membebani server BPS, data siap dianalisis dengan metodologi ekonometrika yang valid. |
| **16** | **Iterative Gap Analysis Protocol (`refine.md`)** | Metodologi perluasan bertahap: Data Dinamis $\rightarrow$ Sensus $\rightarrow$ EXIM $\rightarrow$ BRS Publikasi. | Memastikan CLI dapat diperluas secara teratur tanpa mengganggu stabilitas modul yang sudah ada. |

---

## 3. Struktur Direktori Proyek Standar Produksi

Struktur ditata sesuai hierarki namespace package HKUDS dan Antigravity Plugin:

```text
sbps_api_skill/
├── plugin.json                       # Konfigurasi Antigravity Plugin
├── setup.py                          # Registrasi Global Binary `bps` (PEP 420)
├── BPS.md                            # Dokumen Arsitektur API BPS & Domain Boundary
├── coverage.matrix.json              # Kontrak Pemetaan Fitur, Endpoint & Tests
├── grand_plan_bps_api_cli.md         # Dokumen Master Plan ini
├── README.md                         # Panduan Lengkap Manusia
├── TEST.md                           # Dokumentasi Rencana & Hasil Uji Agent Journeys
├── .env                              # BPS_API_KEY & Konfigurasi Lokal
├── .env.example                      # Template Environment Aman
├── .bps_session.json                 # State Sesi Aktif (Gitignored)
├── trajectory.json                   # Log Replay Riwayat Riset (Gitignored)
│
├── skills/
│   └── bps-api/
│       └── SKILL.md                  # SOP Kanonikal Agen Antigravity (Auto-generated)
│
├── cli_anything/                     # Namespace Root (NO __init__.py sesuai PEP 420)
│   └── bps/                          # Regular Sub-package (HAS __init__.py)
│       ├── __init__.py
│       ├── bps_cli.py                # Main Entry Point, Click Groups & Piped REPL Guard
│       │
│       ├── core/                     # Logika Inti & Engine
│       │   ├── __init__.py
│       │   ├── api.py                # HTTP Engine, WAF Backoff, Composite Matrix Decoder
│       │   ├── cache.py              # Local SQLite Caching untuk Domain & Subjek
│       │   ├── audit.py              # Search, Probe & Harmonization Engine
│       │   ├── session.py            # Session Stack, Windows msvcrt / fcntl Locking & Undo/Redo
│       │   └── preview.py            # Preview Protocol Builder (summary.json & SHA-256 Cache)
│       │
│       ├── utils/                    # Helper & Integrasi Sistem
│       │   ├── __init__.py
│       │   ├── repl_skin.py          # Terminal Skin, Banner & Prompt-Toolkit
│       │   ├── stream.py             # Windows-Safe ASCII Encoder & Logger
│       │   ├── error_handler.py      # Decorator @handle_error & JSON Stderr Emitter
│       │   └── skill_generator.py    # Generator AST Otomatis untuk SKILL.md
│       │
│       └── tests/                    # Test Harness Suite
│           ├── __init__.py
│           ├── conftest.py           # Synthetic Mock Fixtures & _resolve_cli helper
│           ├── test_core.py          # Unit Test (Synthetic Data Only)
│           ├── test_full_e2e.py      # E2E Test dengan Subprocess & Readiness Check
│           ├── test_journeys.py      # Multi-step Agent Research Journeys
│           └── test_validate.py      # Validator Kepatuhan Standar HARNESS.md
│
├── scripts/
│   └── verify_harness.py             # Skrip Verifikasi Mandiri Struktur & Kualitas
│
└── data/                             # Direktori Output Data & Preview Bundles (Gitignored)
    └── previews/
```

---

## 4. Spesifikasi Perintah CLI Surface Lengkap

Seluruh perintah CLI mendukung opsi universal:
* `--json` : Mengaktifkan output mesin (JSON murni di `stdout`).
* `--session <path>` : Menggunakan file sesi khusus (default: `.bps_session.json`).
* `--domain <id/nama>` : Mengesampingkan domain untuk pemanggilan saat itu.

### A. Readiness Probe & Status (`bps status` / `bps ping`)
```bash
# Cek kesiapan sistem, koneksi API BPS, dan usia cache lokal
bps status --json
```

### B. Manajemen Sesi & Trajectory (`bps session`)
```bash
# Inisialisasi sesi riset baru
bps session init --domain 3500 --name "Riset_Kemiskinan_Jatim"

# Cek status sesi (domain aktif, subjek aktif, snapshot level)
bps session status --json

# Ubah domain aktif (otomatis disimpan ke sesi)
bps session set-domain 3300

# Mundur satu langkah jika agen salah pilih parameter
bps session undo

# Maju kembali satu langkah
bps session redo

# Lihat rekam jejak eksekusi dari trajectory.json
bps session history --limit 10 --json

# Reset sesi kembali ke default nasional (0000)
bps session reset
```

### C. Audit & Ketersediaan Data (`bps audit` & `bps inspect`)
```bash
# 1. Audit topik riset secara menyeluruh
bps audit --topic "kemiskinan" --json

# 2. Inspeksi mendalam satu variabel tertentu
bps inspect --var 123 --json
```

### D. Data Preview Protocol dengan SHA-256 Cache (`bps preview`)
```bash
# Menghasilkan preview bundle tanpa mengunduh data utuh
bps preview --var 123 --th 126 --json
```

### E. Keamanan & Penarikan Data (`bps fetch`)
```bash
# 1. Cek keamanan kuota/request terlebih dahulu (Dry-Run)
bps fetch --var 123 --th 126 --format csv --dry-run --json

# 2. Eksekusi penarikan data ke file CSV lokal
bps fetch --var 123 --th 126 --format csv --output data/kemiskinan_jatim_2023.csv
```

### F. Mode REPL Interaktif (`bps repl` atau `bps`)
* Jika dipanggil di terminal interaktif: membuka *rich shell* dengan `repl_skin.py`.
* Jika di-pipe (`printf 'help\nexit\n' | bps`): otomatis beralih ke *plain input fallback* tanpa error Windows buffer.

### G. Developer & Tooling Commands
```bash
# Sinkronisasi otomatis SKILL.md dari kode Python via AST
python -m cli_anything.bps.utils.skill_generator

# Verifikasi kepatuhan seluruh harness
python scripts/verify_harness.py
```

---

## 5. Implementasi Kritis: Windows Locking, AST Generator & Content Cache

### A. Pola `_locked_save_json` (Windows `msvcrt` + POSIX `fcntl`)
Di dalam `cli_anything/bps/core/session.py`:
```python
import json
import os
from pathlib import Path
from typing import Any

def _locked_save_json(path: Path, data: dict[str, Any], **dump_kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        handle = path.open("r+", encoding="utf-8")
    except FileNotFoundError:
        handle = path.open("w+", encoding="utf-8")
        
    with handle:
        locked = False
        try:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            locked = True
        except (ImportError, OSError):
            try:
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
                locked = True
            except (ImportError, OSError):
                pass
                
        try:
            handle.seek(0)
            handle.truncate()
            json.dump(data, handle, **dump_kwargs)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        finally:
            if locked:
                try:
                    import fcntl
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
                except (ImportError, OSError):
                    try:
                        import msvcrt
                        handle.seek(0)
                        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                    except (ImportError, OSError):
                        pass
```

### B. Content-Addressable Preview Cache (`fingerprint_data`)
Di dalam `cli_anything/bps/core/preview.py`:
```python
import hashlib
import json
from typing import Any

def fingerprint_data(data: Any) -> str:
    serialized = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return f"sha256:{hashlib.sha256(serialized.encode('utf-8')).hexdigest()}"

def get_preview_cache_key(var_id: int, th: int, domain: str) -> str:
    return fingerprint_data({
        "protocol": "preview-bundle/v1",
        "var_id": var_id,
        "th": th,
        "domain": domain
    })
```

---

## 6. Spesifikasi Kontrak Keterlacakan (`coverage.matrix.json`)

File `coverage.matrix.json` di root direktori memetakan setiap skenario ke tes otomatis:
```json
{
  "software": "BPS-Web-API",
  "workflows": [
    {
      "use_case": "Probe status ketersediaan server dan validitas API Key",
      "cli_commands": ["bps status --json"],
      "backend_interfaces": ["GET /api/list/model/data/lang/ind/domain/0000/key/..."],
      "unit_tests": ["test_api_ping_mock"],
      "e2e_tests": ["test_e2e_status_command"]
    },
    {
      "use_case": "Audit ketersediaan data topik riset kemiskinan dan ketimpangan",
      "cli_commands": ["bps audit --topic kemiskinan --json"],
      "backend_interfaces": [
        "GET /api/list/model/subject/lang/ind/domain/.../key/...",
        "GET /api/list/model/var/lang/ind/domain/.../key/..."
      ],
      "unit_tests": ["test_audit_topic_matching", "test_audit_papua_anomaly"],
      "e2e_tests": ["test_e2e_audit_journey"]
    },
    {
      "use_case": "Generate data preview bundle dan summary.json dengan SHA-256 cache",
      "cli_commands": ["bps preview --var 123 --th 126 --json"],
      "backend_interfaces": ["GET /api/list/model/data/lang/ind/domain/.../var/123/th/126/key/..."],
      "unit_tests": ["test_preview_summary_stats", "test_preview_cache_hit"],
      "e2e_tests": ["test_e2e_preview_bundle_created"]
    },
    {
      "use_case": "Ekspor data final ke CSV dengan verifikasi dry-run",
      "cli_commands": [
        "bps fetch --var 123 --th 126 --dry-run --json",
        "bps fetch --var 123 --th 126 --format csv --output <file>"
      ],
      "backend_interfaces": ["GET /api/list/model/data/lang/ind/domain/.../key/..."],
      "unit_tests": ["test_dry_run_request_calculator"],
      "e2e_tests": ["test_e2e_fetch_csv_written"]
    }
  ]
}
```

---

## 7. Rencana Pengujian Komprehensif (`TEST.md`)

Pengujian disusun dalam dua bagian sesuai standar `validate.md` HKUDS:

### Bagian 1: Test Plan
* **Unit Tests (`test_core.py`):**
  * Pengujian murni dengan data sintesis (*mock HTTP*) tanpa koneksi internet.
  * Uji composite key decoder BPS (`verval + var + turvar + tahun + turth`).
  * Uji session stack undo/redo (memastikan snapshot kembali presisi).
  * Uji atomic file locking pada Windows `msvcrt` dan Linux `fcntl`.
  * Uji cache hit SHA-256 pada modul preview.
* **E2E Subprocess Tests (`test_full_e2e.py`):**
  * Menggunakan helper `_resolve_cli("bps")` (mendukung `CLI_ANYTHING_FORCE_INSTALLED`).
  * Memastikan binary dapat dipanggil dari sembarang direktori (`cwd` independen).
  * Memastikan `stdout` bersih JSON dan `stderr` menangkap error terstruktur.
* **Agent User Journeys (`test_journeys.py`):**
  * *Journey A (Readiness & Macro):* `bps status --json` $\rightarrow$ `bps indicators --json`.
  * *Journey B (Regional Research):* `session init` $\rightarrow$ `audit --topic kemiskinan` $\rightarrow$ `preview` $\rightarrow$ `fetch --dry-run` $\rightarrow$ `fetch --output`.
  * *Journey C (Undo Recovery):* Menguji agen salah memasukkan domain lalu mengeksekusi `session undo`.

### Bagian 2: Test Results & Validation Checklist
* Seluruh hasil eksekusi pytest dicatat dengan tingkat kelulusan 100% (*100% pass rate*).
* Skrip `test_validate.py` dijalankan untuk memastikan seluruh aturan HARNESS.md terpenuhi.

---

## 8. Roadmap Implementasi Bertahap (Milestones)

```text
┌────────────────────────────────────────────────────────────────────────┐
│ MILESTONE 1: Namespace Packaging, Windows Locks & Stream Resilience    │
│ • Susun paket `cli_anything.bps` & `setup.py` untuk executable `bps`   │
│ • Implementasikan atomic locking (msvcrt/fcntl) di `core/session.py`   │
│ • Implementasikan decorator `@handle_error` & safe ASCII stream        │
├────────────────────────────────────────────────────────────────────────┤
│ MILESTONE 2: Readiness Probe, Session Stack & Trajectory               │
│ • Buat perintah `bps status` (readiness & latency check)               │
│ • Implementasikan 50-level snapshot stack & append-only trajectory.json│
├────────────────────────────────────────────────────────────────────────┤
│ MILESTONE 3: Local Caching & Data Availability Audit Engine            │
│ • Buat `core/cache.py` (SQLite caching untuk domain & subjek)          │
│ • Buat `core/audit.py` (probe ketersediaan, anomali Papua, BRS match)  │
│ • Daftarkan perintah: `bps audit`, `bps inspect`, `bps cache`          │
├────────────────────────────────────────────────────────────────────────┤
│ MILESTONE 4: Preview Protocol dengan SHA-256 & Safety Dry-Run          │
│ • Buat `core/preview.py` untuk emisi bundle `summary.json`             │
│ • Tambahkan algoritma fingerprinting SHA-256 untuk preview cache       │
│ • Tambahkan flag `--dry-run` untuk kalkulasi kuota WAF                 │
│ • Daftarkan perintah: `bps preview`, `bps fetch`                       │
├────────────────────────────────────────────────────────────────────────┤
│ MILESTONE 5: REPL Skin, AST Skill Sync & Antigravity Packaging         │
│ • Implementasikan `utils/repl_skin.py` dengan fallback terminal piped  │
│ • Buat `utils/skill_generator.py` untuk auto-sync `SKILL.md` via AST   │
│ • Tulis dokumen arsitektur domain `BPS.md` & `coverage.matrix.json`    │
│ • Konfigurasi file Antigravity `plugin.json`                           │
├────────────────────────────────────────────────────────────────────────┤
│ MILESTONE 6: Testing Harness, Validator & TEST.md Verification         │
│ • Tulis unit test sintesis, E2E subprocess, dan Agent Journeys         │
│ • Buat `scripts/verify_harness.py` untuk uji kepatuhan otomatis        │
│ • Jalankan validasi HARNESS dan publikasikan laporan `TEST.md`         │
└────────────────────────────────────────────────────────────────────────┘
```

---
*Dokumen Master Plan ini merupakan spesifikasi lengkap, final, dan definitif yang siap dieksekusi.*
