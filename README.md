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

## 📚 Dokumen Spesifikasi Penting

* [grand_plan_bps_api_cli.md](./grand_plan_bps_api_cli.md): Dokumen Master Plan spesifikasi lengkap 16 pilar.
* [BPS.md](./BPS.md): Spesifikasi arsitektur domain, rute URL, dan formula dekoder matriks komposit BPS.
* [coverage.matrix.json](./coverage.matrix.json): Kontrak keterlacakan antara Use Case, CLI, Endpoint, dan Test.
* [TEST.md](./TEST.md): Rencana pengujian dan hasil eksekusi pengujian otomatis.
* [.agents/skills/bps-api/SKILL.md](./.agents/skills/bps-api/SKILL.md): Panduan SOP resmi untuk AI Agent Antigravity.
