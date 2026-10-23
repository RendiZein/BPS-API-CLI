---
name: bps-api-analyst
description: Autonomous Indonesian statistical data researcher and availability auditor using official BPS Web API.
tags: [bps, statistics, economics, indonesia, data-audit]
---

# BPS Data Analyst & Auditor Skill

Gunakan skill ini ketika pengguna mengajukan pertanyaan riset ekonomi/sosial, memerlukan data statistik resmi Indonesia (BPS), atau ingin menganalisis fenomena empiris.

## 5 Golden Rules For AI Agents
1. **Always use `--json` flag** pada setiap eksekusi perintah terminal untuk mendapatkan output yang deterministik.
2. **Check return codes** (0 untuk sukses, non-zero untuk error).
3. **Parse stderr on failure:** Jika perintah gagal, tangkap objek JSON error dari `stderr` untuk memahami kode mitigasinya.
4. **Use absolute paths** untuk argumen `--output` dan verifikasi bahwa file fisik benar-benar ada di disk sebelum melapor ke pengguna.
5. **Probe Before Fetching:** Dilarang keras memanggil `fetch` sebelum menjalankan `audit` atau `inspect` dan menyajikan proposal opsi riset kepada pengguna.

## Standard Operating Procedure (Alur Riset AI)
- **Langkah 0 (Readiness):** Jalankan `bps status --json` untuk memverifikasi koneksi API dan latensi server.
- **Langkah 1 (Sesi):** Identifikasi wilayah riset. Jika provinsi/kabupaten, jalankan `bps session set-domain <id>` (atau gunakan nama wilayah langsung).
- **Langkah 2 (Audit):** Jalankan `bps audit --topic "<topik>" --json` untuk memeriksa ketersediaan variabel dan rentang tahun.
- **Langkah 3 (Harmonisasi & Formulasi):** 
  - Evaluasi rentang tahun yang tersedia.
  - Periksa anomali pemekaran wilayah dan perbedaan frekuensi (bulanan vs tahunan).
  - Sajikan 2-3 proposal riset metodologis kepada pengguna (misal: Regresi Panel vs Analisis Tren).
- **Langkah 4 (Preview):** Setelah pengguna menyetujui opsi, jalankan `bps preview --var <id> --th <th_id> --json` untuk membaca `summary.json`.
- **Langkah 5 (Ekspor):** Jalankan `bps fetch --var <id> --th <th_id> --format csv --output <path>` dan berikan kesimpulan awal data.

## Command Reference

| Command | Description |
| :--- | :--- |
| `bps repl` | Start interactive REPL mode (or plain fallback if piped). |
| `bps status` | Check BPS API connection readiness, latency, and key validity. |
| `bps init` | Initialize a research session state. |
| `bps status` | View active session state and snapshot stack depth. |
| `bps set-domain` | Set active domain ID for the current session. |
| `bps undo` | Undo the last session action. |
| `bps redo` | Redo the last undone session action. |
| `bps reset` | Reset session state to default national domain (0000). |
| `bps indicators` | Fetch Strategic Macroeconomic Indicators (PDRB, Inflation, Poverty, Unemployment, HDI). |
| `bps subject` | List or search statistical subjects. |
| `bps variable` | List statistical variables under a subject. |
| `bps audit` | Audit BPS data availability, time series depth, and research feasibility for a topic. |
| `bps inspect` | Inspect detailed dimensions (vervar, turvar, periods) of a specific variable. |
| `bps sync` | Sync BPS domains and national subjects to local SQLite cache. |
| `bps status` | View local SQLite cache size and sync status. |
| `bps clear` | Clear local SQLite metadata cache. |
| `bps preview` | Generate or retrieve a SHA-256 cached data preview bundle (summary.json). |
| `bps fetch` | Fetch complete dynamic dataset with optional CSV/JSON export and safety dry-run. |

## Examples

### 1. Readiness Check
```bash
bps status --json
```

### 2. Audit Ketersediaan Data Topik Riset
```bash
bps audit --topic "kemiskinan" --domain "Jawa Timur" --json
```

### 3. Inspeksi Dimensi & Kategori Variabel
```bash
bps inspect --var 49 --domain 3500 --json
```

### 4. Data Preview Protocol (Summary & Head/Tail Sample)
```bash
bps preview --var 49 --th 126 --domain 3500 --json
```

### 5. Fetch & Ekspor Data ke CSV (dengan Dry-Run Safety)
```bash
# Cek kalkulasi kuota aman
bps fetch --var 49 --th 126 --domain 3500 --format csv --output data/kemiskinan_jatim_2026.csv --dry-run --json

# Eksekusi penyimpanan data riil
bps fetch --var 49 --th 126 --domain 3500 --format csv --output data/kemiskinan_jatim_2026.csv --json
```

### 6. Manajemen Sesi & Recovery Undo
```bash
bps session init --domain 3500 --name "Riset_Jatim" --json
bps session set-domain 3300 --json
bps session undo --json
```
