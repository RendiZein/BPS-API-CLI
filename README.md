# BPS API Skill & Tooling untuk AI Agent

Repository ini menyediakan **Skill Resmi & Klien BPS (Badan Pusat Statistik) Web API** yang telah diaudit, terverifikasi, dan siap digunakan oleh AI Agent (Antigravity, Cline, Cursor, dsb.) maupun pengembang data science.

---

## 🌟 Fitur Utama

- **Zero External Dependencies**: Dibangun murni menggunakan pustaka standar Python 3 (`urllib`, `json`, `csv`, `argparse`). Tidak memerlukan `pip install`.
- **Anti-Error & Audit-Free**: Telah mengoreksi kesalahan rute pada dokumentasi resmi BPS (seperti path `/api/` yang hilang, parameter `th` wajib, parameter `lang` wajib, dsb.).
- **Automatic Composite Key Decoder**: Otomatis mendekode matriks multi-dimensi numerik BPS (`datacontent`) menjadi baris tabel berlabel rapi.
- **WAF & Rate-Limit Safe**: Header HTTP dirancang bersih untuk menghindari pemblokiran *Perimeter WAF Block*. Dilengkapi *retry backoff* otomatis saat server BPS *overload*.
- **Multi-Format Export**: Mendukung tampilan tabel terminal, JSON murni, dan ekspor langsung ke file `.csv` via argumen `--output`.
- **Dual-Engine Ready (V1 & V2)**: Menggunakan V1 secara default (aktif untuk kunci publik) dan siap beralih ke V2 hanya dengan mengubah baris konfigurasi `.env`.

---

## 🚀 Panduan Memulai Cepat (Quickstart)

### 1. Konfigurasi Lingkungan
Buat file `.env` di direktori utama (contoh tersedia di [.env.example](./.env.example)):

```env
BPS_API_KEY=your_bps_api_key_here
BPS_API_VERSION=v1
BPS_DEFAULT_DOMAIN=0000
BPS_DEFAULT_LANG=ind
```

### 2. Contoh Perintah CLI

```bash
# 1. Cek indikator makroekonomi strategis nasional
python .agents/skills/bps-api/scripts/bps_client.py indicators

# 2. Cari subjek statistik
python .agents/skills/bps-api/scripts/bps_client.py subject --keyword "inflasi"

# 3. Cari variabel di bawah subjek
python .agents/skills/bps-api/scripts/bps_client.py variable --subject 3

# 4. Tarik data dinamis & ekspor ke CSV
python .agents/skills/bps-api/scripts/bps_client.py dynamic-data --var 1753 --th 126 --format csv --output ekspor.csv

# 5. Tarik transaksi perdagangan luar negeri (Exim) per Kode HS
python .agents/skills/bps-api/scripts/bps_client.py exim --kodehs 03 --tahun 2023

# 6. Eksplorasi Sensus Penduduk & Pertanian
python .agents/skills/bps-api/scripts/bps_client.py sensus --action events
```

### 3. Penggunaan sebagai Python Library

```python
import sys, os
sys.path.insert(0, os.path.abspath(".agents/skills/bps-api/scripts"))
from bps_client import BPSClient

client = BPSClient()

# Ambil ringkasan indikator
pagination, indicators = client.get_indicators()

# Ambil & decode dynamic data
raw = client.get_dynamic_data(var_id=1753, th_id=126)
decoded_rows = client.decode_dynamic_data(raw)
# Siap diolah: df = pd.DataFrame(decoded_rows)
```

---

## 📁 Struktur Direktori

```
.
├── .env.example                                      # Template file konfigurasi
├── .gitignore                                        # Proteksi file .env agar token aman
├── README.md                                         # Dokumentasi repositori
├── bps_api_documentation.md                          # Dokumentasi mentah BPS
└── .agents/skills/bps-api/                           # Paket Skill Antigravity
    ├── SKILL.md                                      # Runbook instruksi utama agent
    ├── scripts/
    │   ├── __init__.py                               # Package entry point
    │   └── bps_client.py                             # Klien CLI & SDK Python
    ├── references/
    │   ├── endpoints.md                              # Endpoint terverifikasi bebas bug
    │   ├── domains.md                                # Master 34 domain provinsi
    │   ├── dynamic_data_guide.md                     # Panduan decoding datacontent
    │   └── v1_vs_v2.md                               # Laporan teknis engine V1 vs V2
    ├── examples/                                     # 4 Skrip contoh siap pakai
    └── tests/                                        # Automated test suite (100% pass)
```

---

## 🧪 Menjalankan Pengujian Mandiri

```bash
python -m unittest discover -s .agents/skills/bps-api/tests
```

---

## 📦 Instalasi via `npx skills` (skills.sh)

Skill ini telah kompatibel 100% dengan ekosistem **`npx skills`** (kompatibel dengan berbagai coding agent: Antigravity, Cursor, Cline, Claude Code, GitHub Copilot, Codex, Windsurf, dll.).

### 1. Instalasi ke Proyek Lain Secara Lokal
Jika Anda memiliki proyek lain di komputer Anda dan ingin menambahkan skill ini tanpa copy-paste manual:
```bash
# Di dalam direktori proyek target Anda:
npx skills add /path/ke/sbps_api_skill --skill bps-api -p
```

### 2. Mempublikasikan ke Registri Publik `skills.sh`
`npx skills` menggunakan **GitHub sebagai package registry**. Begitu repositori ini di-push ke GitHub:
1. Buat repository publik di GitHub (misal: `github.com/<username>/sbps_api_skill`).
2. Push repositori ini ke GitHub.
3. Siapa pun (atau Anda di perangkat lain) dapat langsung memasang skill ini:
   ```bash
   # Pasang di level proyek:
   npx skills add <username>/sbps_api_skill --skill bps-api -p
   ```
   Skill ini otomatis terindeks di [skills.sh](https://skills.sh)!
