# BPS Web API Quick Cheatsheet

Referensi cepat URL model, parameter, dan perintah CLI untuk API BPS (v1 & v2).

---

## 1. Ringkasan Endpoint Utama

Base URL: `https://webapi.bps.go.id/v1/api`

| Fungsi | Endpoint URL Format | Parameter Wajib |
| :--- | :--- | :--- |
| **Daftar Domain** | `/domain/type/{prov\|kabbyprov\|all}/key/{key}/` | `type`, `key` |
| **Daftar Subjek** | `/list/model/sub/domain/{domain}/key/{key}/` | `domain`, `key` |
| **Daftar Variabel** | `/list/model/var/domain/{domain}/sub/{sub_id}/key/{key}/` | `domain`, `sub_id`, `key` |
| **Data Dinamis** | `/list/model/data/domain/{domain}/var/{var_id}/key/{key}/` | `domain`, `var_id`, `key` |
| **Berita Resmi (BRS)**| `/list/model/pressrelease/domain/{domain}/key/{key}/` | `domain`, `key` |
| **Publikasi** | `/list/model/publication/domain/{domain}/key/{key}/` | `domain`, `key` |
| **Tabel Statis** | `/list/model/statictable/domain/{domain}/key/{key}/` | `domain`, `key` |
| **Indikator Strategis**| `/list/model/indicators/domain/{domain}/key/{key}/` | `domain`, `key` |

---

## 2. Pemetaan Kode Domain Wilayah Penting

- `0000`: Nasional / BPS Pusat
- `1100` - `1900`: Provinsi di Pulau Sumatera (1100 Aceh, 1200 Sumut, 1300 Sumbar, 1400 Riau, dst.)
- `3100` - `3600`: Provinsi di Pulau Jawa (3100 DKI, 3200 Jabar, 3300 Jateng, 3400 DIY, 3500 Jatim, 3600 Banten)
- `5100` - `5300`: Bali & Nusa Tenggara
- `6100` - `6500`: Kalimantan
- `7100` - `7600`: Sulawesi
- `8100` - `8200`: Maluku & Maluku Utara
- `9100` - `9600`: Papua, Papua Barat, Papua Selatan, Papua Tengah, Papua Pegunungan, Papua Barat Daya

---

## 3. Ekivalensi Perintah CLI

| Endpoint / Tugas | Perintah BPS CLI |
| :--- | :--- |
| Cek status koneksi | `bps status --json` |
| Set domain aktif | `bps session set-domain 3500 --json` |
| Cari variabel topik | `bps audit --topic "kemiskinan" --domain 3500 --json` |
| Inspeksi dimensi | `bps inspect --var 49 --domain 3500 --json` |
| Preview ringkas | `bps preview --var 49 --th 126 --domain 3500 --json` |
| Ekspor dataset | `bps fetch --var 49 --th 126 --format csv --output data/kemiskinan.csv --json` |
