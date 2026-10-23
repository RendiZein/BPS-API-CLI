# Master Domain BPS (Badan Pusat Statistik)

Kode Domain adalah 4 digit identifier wilayah kerja BPS. Kode ini **wajib** digunakan pada hampir semua endpoint BPS Web API.

## 1. Domain Nasional / Pusat

| Domain ID | Nama Wilayah | Portal URL |
| :--- | :--- | :--- |
| `0000` | **Nasional / BPS Pusat** (Default) | https://www.bps.go.id |

## 2. Domain Provinsi (34 Domain Terdaftar)

| Domain ID | Nama Provinsi | URL Web BPS Provinsi |
| :--- | :--- | :--- |
| `1100` | Aceh | https://aceh.bps.go.id |
| `1200` | Sumatera Utara | https://sumut.bps.go.id |
| `1300` | Sumatera Barat | https://sumbar.bps.go.id |
| `1400` | Riau | https://riau.bps.go.id |
| `1500` | Jambi | https://jambi.bps.go.id |
| `1600` | Sumatera Selatan | https://sumsel.bps.go.id |
| `1700` | Bengkulu | https://bengkulu.bps.go.id |
| `1800` | Lampung | https://lampung.bps.go.id |
| `1900` | Kep. Bangka Belitung | https://babel.bps.go.id |
| `2100` | Kep. Riau | https://kepri.bps.go.id |
| `3100` | Dki Jakarta | https://jakarta.bps.go.id |
| `3200` | Jawa Barat | https://jabar.bps.go.id |
| `3300` | Jawa Tengah | https://jateng.bps.go.id |
| `3400` | Di Yogyakarta | https://yogyakarta.bps.go.id |
| `3500` | Jawa Timur | https://jatim.bps.go.id |
| `3600` | Banten | https://banten.bps.go.id |
| `5100` | Bali | https://bali.bps.go.id |
| `5200` | Nusa Tenggara Barat | https://ntb.bps.go.id |
| `5300` | Nusa Tenggara Timur | https://ntt.bps.go.id |
| `6100` | Kalimantan Barat | https://kalbar.bps.go.id |
| `6200` | Kalimantan Tengah | https://kalteng.bps.go.id |
| `6300` | Kalimantan Selatan | https://kalsel.bps.go.id |
| `6400` | Kalimantan Timur | https://kaltim.bps.go.id |
| `6500` | Kalimantan Utara | https://kaltara.bps.go.id |
| `7100` | Sulawesi Utara | https://sulut.bps.go.id |
| `7200` | Sulawesi Tengah | https://sulteng.bps.go.id |
| `7300` | Sulawesi Selatan | https://sulsel.bps.go.id |
| `7400` | Sulawesi Tenggara | https://sultra.bps.go.id |
| `7500` | Gorontalo | https://gorontalo.bps.go.id |
| `7600` | Sulawesi Barat | https://sulbar.bps.go.id |
| `8100` | Maluku | https://maluku.bps.go.id |
| `8200` | Maluku Utara | https://malut.bps.go.id |
| `9100` | Papua Barat | https://papuabarat.bps.go.id |
| `9400` | Papua | https://papua.bps.go.id |

## 3. Domain Kabupaten / Kota (`kab`)

Untuk mencari domain kabupaten/kota tertentu:
- Gunakan CLI helper: `python scripts/bps_client.py domain --type kabbyprov --prov <KODE_PROV>`
- Contoh Jawa Barat (`3200`): `python scripts/bps_client.py domain --type kabbyprov --prov 3200`
- Atau tampilkan seluruh 514 kabupaten/kota: `python scripts/bps_client.py domain --type kab`
