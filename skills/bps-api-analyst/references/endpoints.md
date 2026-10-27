# Referensi Endpoint BPS Web API Terverifikasi

Dokumentasi ini adalah versi **terkoreksi dan terverifikasi secara langsung** dari dokumentasi mentah BPS API. Seluruh bug path URL dan parameter yang ada pada dokumentasi resmi BPS telah diperbaiki di sini.

---

## 1. Aturan Dasar Protokol & Gotchas

> [!IMPORTANT]
> 1. **URL Wajib Menyertakan `/api/`**: Dokumentasi resmi BPS sering keliru menulis `/v1/view` atau `/v1/list`. Pemanggilan tanpa `/api/` akan menghasilkan **HTTP 404**. Format yang benar selalu:
>    `https://webapi.bps.go.id/{version}/api/{action}/...`
> 2. **Pola Parameter Path Segments**: Parameter utama disusun berpasangan di dalam path URL:
>    `.../model/{model}/domain/{domain}/key/{key}/...`
> 3. **Format Respons Sukses (Pola Array 2 Elemen)**:
>    Untuk endpoint `list`, field `data` mengembalikan array berisi dua elemen:
>    - `data[0]`: Metadata pagination (`page`, `pages`, `per_page`, `count`, `total`).
>    - `data[1]`: Array daftar data sebenarnya `[{...}, {...}]`.
> 4. **Format Saat Data Kosong**:
>    Jika data tidak ditemukan atau halaman melebihi total, BPS mengembalikan string kosong `""` pada `data`:
>    `{"status": "OK", "data-availability": "list-not-available", "data": ""}`.
>    Jangan langsung lakukan iterasi pada `data` sebelum memeriksa `isinstance(data, list)`.
> 5. **Deteksi Galat HTTP**:
>    BPS V1 mengembalikan kode HTTP `200 OK` bahkan saat autentikasi gagal. Wajib periksa `response.get("status") == "OK"`.
> 6. **Proteksi WAF (Web Application Firewall)**:
>    Hindari mengirim header seperti `X-Requested-With`, `Referer`, atau `Origin` kustom yang dapat memicu *HTTP 403 Perimeter WAF Block*.

---

## 2. Master Domain Endpoint

Melihat daftar domain (kantor BPS) di seluruh Indonesia.

* **URL**: `https://webapi.bps.go.id/v1/api/domain/type/{type}/key/{key}/`
* **Metode**: `GET`
* **Parameter**:
  * `type` (*wajib*):
    * `all`: Seluruh domain (549 wilayah).
    * `prov`: Hanya domain level provinsi (34 domain).
    * `kab`: Seluruh domain kabupaten/kota (514 domain).
    * `kabbyprov`: Kabupaten/kota di dalam provinsi tertentu (wajib sertakan param `prov`).
  * `prov` (*kondisional*): Kode 4-digit provinsi saat menggunakan `type/kabbyprov/prov/{prov_id}`.
  * `key` (*wajib*): BPS API Key.

---

## 3. Metadata & Navigasi Statistik (`/api/list/`)

Digunakan untuk menelusuri subjek, variabel, dan dimensi sebelum mengambil angka statistik.

### A. Daftar Kategori Subjek (`subcat`)
* **URL**: `https://webapi.bps.go.id/v1/api/list/model/subcat/domain/{domain}/key/{key}/`
* **Contoh Subcat**: Sosial dan Kependudukan (`1`), Ekonomi dan Perdagangan (`2`), Pertanian dan Pertambangan (`3`).

### B. Daftar Subjek (`subject`)
* **URL**: `https://webapi.bps.go.id/v1/api/list/model/subject/domain/{domain}/key/{key}/`
* **Parameter Opsional**:
  * `/subcat/{subcat_id}/`: Filter berdasarkan kategori subjek.
  * `/page/{page}/`: Nomor halaman.
* **Contoh Output**: `sub_id: 40` (Gender), `sub_id: 23` (Inflasi), `sub_id: 12` (Kemiskinan).

### C. Daftar Variabel (`var`)
* **URL**: `https://webapi.bps.go.id/v1/api/list/model/var/domain/{domain}/key/{key}/`
* **Parameter Opsional**:
  * `/subject/{sub_id}/`: Filter variabel untuk subjek tertentu.
  * `/page/{page}/`: Halaman.
* **Output Kunci**: `var_id`, `title`, `unit`, `def`, `notes`.

### D. Daftar Periode / Tahun (`th`)
* **URL**: `https://webapi.bps.go.id/v1/api/list/model/th/domain/{domain}/var/{var_id}/key/{key}/`
* **Catatan**: Endpoint ini **krusial** untuk mencari `th_id` yang valid sebelum memanggil *Dynamic Data*.
* **Output**: `th_id` (misal `126` untuk tahun 2026, `125` untuk 2025).

### E. Dimensi Turunan Lainnya
* **Derived Variable (`turvar`)**: `.../model/turvar/domain/{domain}/var/{var_id}/key/{key}/`
* **Vertical Variable (`vervar`)**: `.../model/vervar/domain/{domain}/var/{var_id}/key/{key}/`
* **Derived Period (`turth`)**: `.../model/turth/domain/{domain}/var/{var_id}/key/{key}/`
* **Unit Data (`unit`)**: `.../model/unit/domain/{domain}/key/{key}/`

---

## 4. Dynamic Data / Tabel Dinamis (`model/data`)

Mengambil data statistik numerik (angka inflasi, ekspor, PDRB, penduduk, dsb.).

* **URL**: `https://webapi.bps.go.id/v1/api/list/model/data/domain/{domain}/var/{var_id}/th/{th_id}/key/{key}/`
* **Parameter Wajib**:
  * `domain`: Kode wilayah (misal `0000`).
  * `var`: ID Variabel (didapat dari `model/var`).
  * `th`: ID Periode data (didapat dari `model/th`). **Parameter ini wajib! Dokumentasi resmi keliru menghilangkannya**.
* **Parameter Opsional**:
  * `/turvar/{turvar_id}/`: ID turunan variabel.
  * `/vervar/{vervar_id}/`: ID baris vertical (misal ID provinsi/kabupaten).
  * `/turth/{turth_id}/`: ID turunan periode (misal bulan Januari, Triwulan 1).
* **Format Output**:
  * Berisi metadata dimensi: `var`, `turvar`, `vervar`, `tahun`, `turtahun`.
  * Berisi angka data pada dictionary `datacontent`:
    ```json
    "datacontent": {
      "1175301261": 891.8,
      "2175301261": 21850.3
    }
    ```
  * *Lihat [dynamic_data_guide.md](./dynamic_data_guide.md) untuk rumus decoding kunci `datacontent`*.

---

## 5. Static Table / Tabel Statis

### A. List Tabel Statis
* **URL**: `https://webapi.bps.go.id/v1/api/list/model/statictable/domain/{domain}/key/{key}/`
* **Parameter Opsional**: `/page/{page}/`, `/keyword/{kata_kunci}/`, `/month/{mm}/`, `/year/{yyyy}/`.

### B. Detail Tabel Statis (Konten Tabel & File Excel)
* **URL**: `https://webapi.bps.go.id/v1/api/view/model/statictable/lang/{lang}/domain/{domain}/id/{table_id}/key/{key}/`
* **Catatan**: Parameter `/lang/ind/` **wajib ada**, jika tidak server menolak dengan pesan *Parameter lang is Missing*.
* **Output**: Berisi judul, HTML tabel pada field `table`, dan tautan unduh file `.xls` resmi BPS pada field `excel`.

---

## 6. Publikasi & Dokumen BPS

### A. List Publikasi
* **URL**: `https://webapi.bps.go.id/v1/api/list/model/publication/domain/{domain}/key/{key}/`
* **Parameter Opsional**: `/page/{page}/`, `/keyword/{kata_kunci}/`, `/month/{mm}/`, `/year/{yyyy}/`.
* **Output**: `pub_id`, `title`, `issn`, `rl_date`, `cover`, `pdf`, `size`.

### B. Detail Publikasi
* **URL**: `https://webapi.bps.go.id/v1/api/view/model/publication/lang/{lang}/domain/{domain}/id/{pub_id}/key/{key}/`
* **Output**: `abstract`, link unduh PDF publikasi lengkap BPS.

---

## 7. Berita Resmi Statistik (BRS / Press Release)

### A. List Press Release
* **URL**: `https://webapi.bps.go.id/v1/api/list/model/pressrelease/domain/{domain}/key/{key}/`
* **Parameter Opsional**: `/page/{page}/`, `/keyword/{kata_kunci}/`, `/month/{mm}/`, `/year/{yyyy}/`.
* **Output**: `brs_id`, `title`, `rl_date`, `pdf`, `slide`, `thumbnail`.

### B. Detail Press Release
* **URL**: `https://webapi.bps.go.id/v1/api/view/model/pressrelease/lang/{lang}/domain/{domain}/id/{brs_id}/key/{key}/`
* **Output**: Teks lengkap rilis pers dan link PDF materi rilis pers.

---

## 8. Indikator Strategis (`indicators`)

Menampilkan ringkasan ringkas indikator makroekonomi (Inflasi, Kemiskinan, Pengangguran, Pertumbuhan Ekonomi, IPM).

* **URL**: `https://webapi.bps.go.id/v1/api/list/model/indicators/domain/{domain}/key/{key}/`
* **Output**: `indicator_id`, `title`, `name`, `value`, `unit`, `periode`, `data_source`.

---

## 9. Perdagangan Luar Negeri (Exim)

Data transaksi ekspor dan impor Indonesia berdasarkan klasifikasi kode Harmonized System (HS Code).

* **URL**: `https://webapi.bps.go.id/v1/api/dataexim/sumber/{sumber}/periode/{periode}/kodehs/{kodehs}/jenishs/{jenishs}/tahun/{tahun}/key/{key}/`
* **Parameter**:
  * `sumber`: `1` (Ekspor), `2` (Impor)
  * `periode`: `1` (Bulanan), `2` (Tahunan)
  * `kodehs`: Nomor kode HS (misal `03` untuk ikan, `09` untuk kopi/rempah, `27` untuk migas)
  * `jenishs`: `1` (2 digit), `2` (full HS Code)
  * `tahun`: Tahun data (misal `2023`)
* **Output**: `tahun`, `kodehs`, `pod` (pelabuhan muat/bongkar), `ctr` (negara tujuan/asal), `value` (USD), `netweight` (Kg).

---

## 10. Sensus Penduduk & Pertanian (Interoperabilitas)

* **Daftar Event Sensus (Code 37)**:
  `https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/sensus/id/37/key/{key}/`
  * Mengembalikan daftar kegiatan: `sp2020` (Sensus Penduduk 2020), `st2023` (Sensus Pertanian 2023), dsb.
* **Topik Sensus (Code 38)**:
  `https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/sensus/id/38/kegiatan/{event_id}/key/{key}/`
* **Variabel Sensus (Code 40)**:
  `https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/sensus/id/40/kegiatan/{event_id}/topik/{topic_id}/key/{key}/`
* **Data Sensus (Code 41)**:
  `https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/sensus/id/41/kegiatan/{event_id}/wilayah_sensus/{wilayah}/dataset/{dataset_id}/key/{key}/`

---

## 11. Berita & Infografis

* **Infografis**: `https://webapi.bps.go.id/v1/api/list/model/infographic/domain/{domain}/key/{key}/`
* **Daftar Berita**: `https://webapi.bps.go.id/v1/api/list/model/news/domain/{domain}/key/{key}/`
* **Detail Berita**: `https://webapi.bps.go.id/v1/api/view/model/news/lang/{lang}/domain/{domain}/id/{news_id}/key/{key}/`
* **Kategori Berita**: `https://webapi.bps.go.id/v1/api/list/model/newscategory/domain/{domain}/key/{key}/`
* **Glosarium Istilah**: `https://webapi.bps.go.id/v1/api/list/model/glosarium/domain/{domain}/key/{key}/`
