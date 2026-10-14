---
name: bps-api
description: >-
  Use this skill whenever the user or agent needs to query statistical data, macroeconomic indicators,
  census figures, static/dynamic tables, publications, or press releases from Badan Pusat Statistik (BPS) Indonesia.
  Provides a verified, battle-tested Python client and CLI to bypass API quirks, handle authentication,
  and decode multi-dimensional statistical matrices into clean tabular formats.
version: 1.0.0
license: MIT
keywords:
  - bps
  - statistics
  - indonesia
  - economics
  - census
  - open-data
---

# BPS (Badan Pusat Statistik) API Skill

Kompilasi pengetahuan, runbook operasional, dan alat bantu (*tooling*) untuk berinteraksi dengan API resmi Badan Pusat Statistik (BPS) Republik Indonesia secara andal tanpa perlu melakukan audit ulang.

---

## 1. Quick Start: Menggunakan CLI Helper

Semua interaksi dengan BPS Web API sebaiknya dijalankan melalui script klien bawaan:
`scripts/bps_client.py` (otomatis membaca konfigurasi dari [.env](file:///c:/Users/rhend/coding/sbps_api_skill/.env)).

```bash
# 1. Cek indikator makroekonomi strategis terkini (Inflasi, Kemiskinan, PDB, Pengangguran, IPM)
python .agents/skills/bps-api/scripts/bps_client.py indicators

# 2. Cari topik statistik (subjek)
python .agents/skills/bps-api/scripts/bps_client.py subject --keyword "inflasi"

# 3. Cari variabel statistik di bawah subjek
python .agents/skills/bps-api/scripts/bps_client.py variable --subject 3

# 4. Ambil dan langsung dekode data statistik numerik (Dynamic Data)
python .agents/skills/bps-api/scripts/bps_client.py dynamic-data --var 1753 --th 126

# 5. Cari publikasi dan unduh dokumen BPS
python .agents/skills/bps-api/scripts/bps_client.py publication --keyword "kemiskinan"

# 6. Cari tabel statis resmi beserta tautan unduh Excel (.xls)
python .agents/skills/bps-api/scripts/bps_client.py statictable --keyword "ekspor"

# 7. Ambil data perdagangan luar negeri (Exim) per Kode HS
python .agents/skills/bps-api/scripts/bps_client.py exim --kodehs 03 --tahun 2023

# 8. Cek kegiatan Sensus BPS (SP2020, ST2023, dsb.)
python .agents/skills/bps-api/scripts/bps_client.py sensus --action events
```

> [!TIP]
> **Format & Ekspor**:
> - Tambahkan `--format json` untuk output JSON terstruktur.
> - Tambahkan `--format csv` untuk format CSV.
> - Tambahkan `--output nama_file.csv` untuk langsung menyimpan hasil ke disk tanpa parsing manual.

---

## 2. Penggunaan Programmatic dalam Kode Python

Modul klien dapat di-import langsung oleh script data science atau agent lain di dalam workspace:

```python
import sys
import os
sys.path.insert(0, os.path.abspath(".agents/skills/bps-api/scripts"))

from bps_client import BPSClient

client = BPSClient()

# Ambil indikator makroekonomi
_, indicators = client.get_indicators()

# Ambil dynamic data dan langsung dekode matriksnya
raw_data = client.get_dynamic_data(var_id=1753, th_id=126)
decoded_rows = client.decode_dynamic_data(raw_data)
# decoded_rows adalah list of dicts siap pakai untuk Pandas DataFrame!
```

---

## 3. Alur Kerja Standar Mengambil Data Statistik (5 Langkah)

Data statistik BPS bersifat multi-dimensi (antar-wilayah, antar-waktu, dan klasifikasi). Ikuti urutan ini:

1. **Tentukan Wilayah (Domain)**:
   * Default: `0000` (Nasional / BPS Pusat).
   * Provinsi: lihat daftar lengkap di [domains.md](./references/domains.md).
   * Kabupaten/Kota: cari dengan `python .../bps_client.py domain --type kabbyprov --prov <KODE_PROV>`.
2. **Cari Subjek (`subject`)**:
   * Jalankan `python .../bps_client.py subject --keyword "<kata_kunci>"`.
   * Catat `sub_id`.
3. **Cari Variabel (`variable`)**:
   * Jalankan `python .../bps_client.py variable --subject <sub_id>`.
   * Catat `var_id`.
4. **Cek Ketersediaan Periode (`period`)**:
   * BPS menggunakan ID periode internal (`th`), bukan tahun kalender bebas.
   * Jalankan `python .../bps_client.py period --var <var_id>`.
   * Catat `th_id` (misal: `126` untuk 2026).
5. **Ambil & Dekode Data (`dynamic-data`)**:
   * Jalankan `python .../bps_client.py dynamic-data --var <var_id> --th <th_id>`.
   * Data langsung terdekripsi dari kunci komposit ke tabel berlabel rapi.

*Untuk rincian algoritma dekode kunci komposit, baca [dynamic_data_guide.md](./references/dynamic_data_guide.md).*

---

## 4. Aturan & Perangkap Kritis API (Wajib Diketahui)

1. **Jalur URL Wajib Memuat `/api/`**:
   * Benar: `https://webapi.bps.go.id/v1/api/list/...`
   * Salah: `https://webapi.bps.go.id/v1/list/...` *(mengembalikan HTTP 404)*.
2. **Dynamic Data Wajib Parameter `th`**:
   * Memanggil `model/data` tanpa `th` akan menghasilkan pesan galat: `'th' parameter is required`.
3. **Endpoint View (Detail) Wajib Parameter `lang`**:
   * Memanggil `view/model/...` tanpa `/lang/ind/` akan menghasilkan galat: `Parameter lang is Missing`.
4. **Data Kosong Menghasilkan String `""`**:
   * Jika tidak ada hasil, respons berupa `{"status": "OK", "data-availability": "list-not-available", "data": ""}`.
   * Script `bps_client.py` telah menangani kasus ini agar mengembalikan list kosong `[]`.
5. **Autentikasi HTTP 200 Masquerading**:
   * BPS V1 mengembalikan kode HTTP `200 OK` bahkan saat kunci API salah. Selalu periksa `response.get("status") == "OK"`.
6. **Proteksi WAF (Web Application Firewall)**:
   * Jangan mengirim header kustom seperti `X-Requested-With`, `Referer`, atau `Origin` sembarangan karena akan memicu `403 Perimeter WAF Block`. Gunakan header standar `bps_client.py`.

---

## 5. Status Versi BPS API (V1 vs V2)

* **V1 (`https://webapi.bps.go.id/v1/api`)**:
  * Versi **aktif untuk publik**. Kunci API pengembang yang dibuat di portal BPS berjalan di versi ini.
* **V2 (`https://webapi.bps.go.id/v2/api`)**:
  * Engine versi 2.0.0 sudah ada di server BPS, namun kunci API pengembang publik saat ini masih ditolak dengan galat `ERRAUTH002` (memerlukan hak akses khusus).
  * Klien `bps_client.py` dirancang siap pakai (*future-proof*). Cukup ubah `BPS_API_VERSION=v2` di [.env](file:///c:/Users/rhend/coding/sbps_api_skill/.env) jika akun Anda telah diberi izin V2.

*Untuk rincian komparasi teknis, baca [v1_vs_v2.md](./references/v1_vs_v2.md).*

---

## 6. Direktori Resep & Contoh Penggunaan

Lihat folder `examples/` untuk skrip Python mandiri siap pakai:
* :bulb: [01_macro_indicators.py](./examples/01_macro_indicators.py): Menarik ringkasan makroekonomi strategis.
* :bulb: [02_fetch_and_export_inflation.py](./examples/02_fetch_and_export_inflation.py): Menarik data dinamis dan menyimpannya ke CSV.
* :bulb: [03_provincial_comparison.py](./examples/03_provincial_comparison.py): Komparasi statistik lintas provinsi (DKI, Jabar, Jatim, Bali).
* :bulb: [04_foreign_trade_exim.py](./examples/04_foreign_trade_exim.py): Menarik data ekspor/impor komoditas berdasarkan Kode HS.

---

## 7. Pengujian Otomatis (Testing)

Jalankan suite pengujian mandiri kapan saja untuk memverifikasi integritas API dan fungsi dekoding:
```bash
python -m unittest discover -s .agents/skills/bps-api/tests
```

---

## 8. Indeks Dokumen Referensi

* :file_folder: [endpoints.md](./references/endpoints.md): Daftar lengkap endpoint BPS terverifikasi (termasuk Exim & Sensus).
* :earth_asia: [domains.md](./references/domains.md): Master kode 34 provinsi dan cara mencari 514 kabupaten/kota.
* :bar_chart: [dynamic_data_guide.md](./references/dynamic_data_guide.md): Panduan dimensi, matriks data, dan decoding `datacontent`.
* :bookmark_tabs: [v1_vs_v2.md](./references/v1_vs_v2.md): Dokumentasi investigasi teknis V1 vs V2.
* :snake: [bps_client.py](./scripts/bps_client.py): Kode sumber klien & CLI Python.
