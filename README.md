# BPS Agent-Native CLI Suite & Antigravity Skill
> Autonomous Statistical Researcher & Data Availability Auditor for Badan Pusat Statistik (BPS) Indonesia  
> Mengikuti Standar Arsitektur Penuh **HKUDS/CLI-Anything**

---

## 🌟 Ikhtisar Proyek

Repository ini menyediakan **BPS Agent-Native CLI Suite & Antigravity Skill** yang dirancang khusus untuk AI Agent (Antigravity, Cursor, Claude Code, dsb.) dan peneliti data (think tank, analis kebijakan, akademisi).

Sistem ini tidak sekadar menarik data mentah, melainkan bertindak sebagai **Auditor Kelayakan Data**:
1. **Readiness Probe (`bps status`)**: Memeriksa konektivitas dan latensi Web API BPS.
2. **Probe Before Action (`bps audit`)**: Menilai ketersediaan rentang tahun, level wilayah, dan mendeteksi anomali pemekaran wilayah (Papua 34 $\rightarrow$ 38) sebelum mengunduh data.
3. **Data Preview Protocol (`bps preview`)**: Emisi bundle `summary.json` hemat token dengan *content-addressable cache* SHA-256.
4. **Safety Guard (`--dry-run`)**: Menghitung kuota panggilan HTTP dan jeda aman sebelum eksekusi riil untuk menghindari pemblokiran WAF.
5. **Stateful Session Stack**: Penguncian berkas atomik cross-platform (`msvcrt` di Windows, `fcntl` di POSIX) dengan *undo/redo* 50 level dan rekam jejak riset di `trajectory.json`.
6. **AST Auto-Sync `SKILL.md`**: Dokumentasi agen diperbarui otomatis dari kode Python via AST parser.

---

## 🚀 Panduan Memulai Cepat (Quickstart)

### 1. Instalasi Paket (Editable Mode)
```bash
python -m pip install -e .
```

### 2. Konfigurasi Lingkungan (`.env`)
Salin contoh file `.env.example` menjadi `.env`:
```env
BPS_API_KEY=kunci_api_bps_anda_di_sini
BPS_API_VERSION=v1
BPS_DEFAULT_DOMAIN=0000
BPS_DEFAULT_LANG=ind
```

### 3. Alur Penggunaan CLI

#### A. Cek Kesiapan Server API
```bash
bps status --json
```

#### B. Inisialisasi Sesi & Audit Topik Riset
```bash
# Set domain sesi aktif ke Jawa Timur (3500)
bps session init --domain 3500 --name "Riset_Jatim_2026" --json

# Audit ketersediaan data untuk topik kemiskinan
bps audit --topic "kemiskinan" --json

# Inspeksi kategori vertikal dan rentang tahun variabel
bps inspect --var 49 --json
```

#### C. Data Preview Protocol (Hemat Token)
```bash
# Menghasilkan summary.json dan sampel data (otomatis di-cache dengan SHA-256)
bps preview --var 49 --th 126 --json
```

#### D. Penarikan Data Aman (Dry-Run & Export)
```bash
# 1. Cek kuota aman terlebih dahulu
bps fetch --var 49 --th 126 --format csv --output data/kemiskinan_2026.csv --dry-run --json

# 2. Eksekusi penarikan data ke file CSV
bps fetch --var 49 --th 126 --format csv --output data/kemiskinan_2026.csv --json
```

#### E. Pemulihan Sesi (Undo / Redo)
```bash
# Jika salah ubah domain
bps session set-domain 3300 --json
bps session undo --json
```

---

## 🧪 Verifikasi Kepatuhan & Pengujian

Jalankan skrip validator mandiri untuk memverifikasi seluruh komponen harness:
```bash
python scripts/verify_harness.py
```

Jalankan test suite pytest (100% passing):
```bash
python -m pytest cli_anything/bps/tests -v
```

---

## 📁 Struktur Direktori Proyek

```text
BPS-API-CLI/
├── cli_anything/                    # Package Python (PEP 420 Namespace)
│   └── bps/                         # Implementasi Core BPS CLI & Engine
│       ├── core/                    # API Client, SQLite Cache, Audit, Preview, Session
│       ├── utils/                   # REPL Skin, Error Handler, Stream, Skill Generator
│       └── tests/                   # Pytest Unit & E2E Subprocess Tests
├── skills/                          # Kanonikal AI Agent Skills
│   └── bps-api/
│       └── SKILL.md                 # SOP Resmi Agen (Auto-generated via AST)
├── references/                      # Arsip & Referensi Arsitektur BPS
│   ├── ARCHITECTURE.md              # Blueprint Teknis Web API BPS
│   ├── BPS_API_CHEATSHEET.md        # Ringkasan Cepat Endpoint & Parameter
│   └── STATISTICAL_METHODOLOGY.md   # Metodologi Pembacaan Data Statistik BPS
├── examples/                        # Resep Skrip Python Praktis
│   ├── 01_macro_indicators.py       # PDB, Inflasi, Kemiskinan Nasional
│   ├── 02_fetch_and_export_inflation.py # Penarikan & Ekspor Inflasi Bulanan
│   ├── 03_provincial_comparison.py  # Komparasi Indikator Lintas Provinsi
│   └── 04_foreign_trade_exim.py     # Data Ekspor/Impor per Kode HS
├── scripts/                         # Skrip Utilitas & Harness
│   └── verify_harness.py            # Automated Linter & Compliance Validator
├── BPS.md                           # Spesifikasi Domain & Boundary BPS
├── coverage.matrix.json             # Traceability Contract (CLI, API, Tests)
├── grand_plan_bps_api_cli.md        # Dokumen Master Plan 16 Pilar
├── plugin.json                      # Antigravity Plugin Manifest
├── setup.py                         # Konfigurasi Instalasi CLI Package
├── TEST.md                          # Rencana & Hasil Pengujian Sistem
└── README.md                        # Dokumentasi Utama
```

---

## 🤖 Integrasi AI Agent & Skill Discovery

### Instalasi Skill ke Antigravity / Agentic Workspace
AI Agent dapat langsung memanfaatkan skill ini dengan mengimpor folder skill:
```bash
npx skills add RendiZein/BPS-API-CLI --skill bps-api -p
```
Atau secara global untuk seluruh workspace:
```bash
npx skills add RendiZein/BPS-API-CLI --skill bps-api -g -y
```

---

## 📚 Dokumen Spesifikasi Penting

* [grand_plan_bps_api_cli.md](./grand_plan_bps_api_cli.md): Dokumen Master Plan spesifikasi lengkap 16 pilar.
* [BPS.md](./BPS.md): Spesifikasi arsitektur domain, rute URL, dan formula dekoder matriks komposit BPS.
* [coverage.matrix.json](./coverage.matrix.json): Kontrak keterlacakan antara Use Case, CLI, Endpoint, dan Test.
* [TEST.md](./TEST.md): Rencana pengujian dan hasil eksekusi pengujian otomatis.
* [skills/bps-api/SKILL.md](./skills/bps-api/SKILL.md): Panduan SOP resmi untuk AI Agent Antigravity.
