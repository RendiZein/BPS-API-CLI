# BPS Agent-Native CLI Harness Test Plan & Verification

Dokumen ini mencatat rencana pengujian (*Part 1*) dan hasil pengujian aktual (*Part 2*) untuk suite BPS Agent-Native CLI Harness sesuai standar **HKUDS/CLI-Anything**.

---

## Part 1: Test Plan

### 1. Test Inventory
* `test_core.py`: 7 pengujian unit sintetis (*backend-free / mock HTTP*).
* `test_full_e2e.py`: 3 pengujian subprocess nyata menguji isolasi stream `stdout`/`stderr` dan alur agen.
* `scripts/verify_harness.py`: Skrip linter mandiri untuk verifikasi kepatuhan arsitektur plugin.

### 2. Unit Test Scenarios
* **`test_session_state_and_store`**: Memverifikasi penyimpanan status sesi, snapshot history 50 level, serta pemulihan mundur (*undo*) dan maju (*redo*).
* **`test_atomic_file_locking_windows`**: Menguji penguncian berkas atomik di Windows menggunakan `msvcrt` untuk mencegah korupsi data sesi.
* **`test_composite_key_decoder`**: Memverifikasi algoritma pemetaan matriks multi-dimensi komposit BPS (`verval + var + turvar + tahun + turth`).
* **`test_preview_statistics`**: Menguji kalkulasi statistik ringkas (*min, max, mean, median, std_dev*).
* **`test_preview_protocol_cache`**: Memverifikasi emisi bundle `preview-bundle/v1` dan efektivitas *content-addressable cache* SHA-256.
* **`test_local_sqlite_cache`**: Menguji skema SQLite lokal, pembersihan file handle Windows, dan pencarian fuzzy domain/nama daerah.
* **`test_audit_papua_anomaly`**: Memverifikasi deteksi dini pemekaran 38 provinsi Papua tahun 2022 dan formulasi proposal riset.

### 3. Realistic Agent User Journeys (E2E)
* **Journey A (Readiness Probe):** Agen menjalankan `bps status --json` untuk memverifikasi latensi jaringan dan validitas API Key sebelum memulai riset.
* **Journey B (Discovery & Audit):** Agen menjalankan `bps audit --topic "kemiskinan" --domain "Jawa Timur" --json` dan menerima matriks ketersediaan tahun.
* **Journey C (Session & Undo Recovery):** Agen mengubah domain ke Jawa Tengah, lalu menjalankan `bps session undo` untuk kembali ke Jawa Timur.
* **Journey D (Preview & Safe Export):** Agen meminta preview statistik `bps preview --var 49 --th 126 --json`, mengecek kuota `bps fetch --dry-run`, dan mengekspor data bersih ke file `.csv`.

---

## Part 2: Test Results & Verification

### 1. Pytest Test Suite Run
Dijalankan pada platform Windows (Python 3.14.2):

```text
$ python -m pytest cli_anything/bps/tests -v
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: C:\Users\rhend\coding\sbps_api_skill
collected 10 items

cli_anything/bps/tests/test_core.py::test_session_state_and_store PASSED [ 10%]
cli_anything/bps/tests/test_core.py::test_atomic_file_locking_windows PASSED [ 20%]
cli_anything/bps/tests/test_core.py::test_composite_key_decoder PASSED   [ 30%]
cli_anything/bps/tests/test_core.py::test_preview_statistics PASSED      [ 40%]
cli_anything/bps/tests/test_core.py::test_preview_protocol_cache PASSED  [ 50%]
cli_anything/bps/tests/test_core.py::test_local_sqlite_cache PASSED      [ 60%]
cli_anything/bps/tests/test_core.py::test_audit_papua_anomaly PASSED     [ 70%]
cli_anything/bps/tests/test_full_e2e.py::test_e2e_help_subprocess PASSED [ 80%]
cli_anything/bps/tests/test_full_e2e.py::test_e2e_status_json PASSED     [ 90%]
cli_anything/bps/tests/test_full_e2e.py::test_e2e_session_workflow PASSED [100%]

============================= 10 passed in 2.88s ==============================
```

### 2. Harness Compliance Verification (`verify_harness.py`)

```text
$ python scripts/verify_harness.py
============================================================
BPS Agent-Native Harness Compliance Verification
============================================================

[1] Checking Required Files & Specifications:
  [OK] Antigravity Plugin Manifest: plugin.json
  [OK] PEP 420 Packaging Setup: setup.py
  [OK] Domain Architecture Specification: BPS.md
  [OK] Traceability & Coverage Contract: coverage.matrix.json
  [OK] Canonical Agent SKILL.md: .agents/skills/bps-api/SKILL.md
  [OK] Grand Master Plan: grand_plan_bps_api_cli.md

[2] Validating JSON Manifests:
  [OK] Valid JSON: plugin.json
  [OK] Valid JSON: coverage.matrix.json

[3] Validating SKILL.md Frontmatter:
  [OK] SKILL.md YAML frontmatter is valid

[4] Running Pytest Test Suite:
  [OK] Test Suite: 100% Passing (10 passed in 2.88s)

============================================================
[SUCCESS] All validation checks PASSED! Harness is production-ready.
============================================================
```

---
*Laporan pengujian ini memvalidasi bahwa seluruh komponen sistem telah 100% lulus uji dan siap digunakan di lingkungan produksi Antigravity.*
