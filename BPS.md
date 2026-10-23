# BPS Web API Architecture & Harness Specification

Dokumen ini merupakan spesifikasi teknis resmi untuk integrasi AI Agent dan otomasi data dengan Web API Badan Pusat Statistik (BPS) Republik Indonesia.

---

## 1. Batasan API & URL Routing

Web API BPS menggunakan pola URL berbasis *path segments* (bukan query string standar untuk parameter utama):

```text
https://webapi.bps.go.id/{version}/api/{action}/{param1}/{val1}/{param2}/{val2}/key/{key}/
```

* **Versi Default**: `v1` (mendukung kunci API publik secara penuh).
* **Versi Lanjutan**: `v2` (memerlukan bearer token atau persetujuan khusus).
* **Parameter Wajib**:
  * `key`: Kunci API pengguna (harus selalu menjadi segmen terakhir path sebelum trailing slash).
  * `domain`: Kode domain wilayah (default `0000` untuk Nasional).
  * `lang`: Bahasa respons (`ind` atau `eng`).
  * `th`: ID periode/tahun (wajib pada model data dinamis `model/data`).

---

## 2. Struktur Respons BPS & Pola Unwrapping

Sebagian besar respons daftar (*list endpoints*) BPS membungkus data dalam array dua elemen:

```json
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 5,
      "total": 50,
      "count": 10
    },
    [
      {"val": "1", "label": "Record 1"},
      {"val": "2", "label": "Record 2"}
    ]
  ]
}
```

* **Elemen 0**: Metadata paginasi (`page`, `pages`, `total`, `count`).
* **Elemen 1**: Array item data aktual.
* **Kasus Khusus**: Jika data kosong, BPS mengembalikan string kosong `"data": ""` alih-alih array kosong. Klien harus menangani ini tanpa crash.

---

## 3. Formula Dekoder Matriks Komposit (`datacontent`)

Pada model data dinamis (`model/data`), nilai numerik tidak disimpan sebagai baris tabel biasa, melainkan sebagai *dictionary hash* komposit dengan kunci gabungan:

```text
Composite Key = {vervar_val}{var_val}{turvar_val}{tahun_val}{turtahun_val}
```

* `vervar_val`: Nilai klasifikasi vertikal (misal: ID Kabupaten/Kota).
* `var_val`: ID variabel statistik.
* `turvar_val`: ID klasifikasi turunan (misal: Total, Laki-laki, Perempuan).
* `tahun_val`: ID tahun rilis.
* `turtahun_val`: ID periode turunan (misal: Semester 1, Triwulan 2, Tahunan).

Klien secara otomatis mengiterasi seluruh kombinasi dimensi ini dan memetakan nilai mentah `datacontent[key]` menjadi baris data berlabel rapi (*flat tabular records*).

---

## 4. Keamanan & Mitigasi WAF Rate-Limit

Server BPS menerapkan Web Application Firewall (WAF) perimeter:
1. **User-Agent**: Harus menyertakan User-Agent yang bersih (`BPS-Agent-Client/1.0`).
2. **Backoff Retries**: Jika server mengembalikan HTTP 5xx atau terjadi *timeout*, klien otomatis melakukan *exponential backoff* ($2^n$ detik).
3. **HTTP 403 Perimeter Block**: Jika kuota harian habis atau frekuensi request terlalu cepat, sistem melempar `BPSRateLimitError` dengan petunjuk waktu jeda yang aman.

---

## 5. Preview Protocol (`preview-bundle/v1`)

Untuk menghemat *context window* AI, setiap inspeksi data emisi bundle di `data/previews/bndl_<hash>/`:
* `manifest.json`: Metadata protokol dan status bundle.
* `summary.json`: Rangkuman statistik (*min, max, mean, median, std_dev, null percentage, shape*) dan sampel data.
* `artifacts/sample.csv`: Sampel 20 baris pertama data tabular.
* **SHA-256 Cache**: Sidik jari parameter mencegah penarikan ulang data yang identik.

---

## 6. Sesi & Trajectory

State sesi tersimpan di `.bps_session.json` dengan penguncian berkas atomik (`msvcrt` di Windows, `fcntl` di POSIX), mendukung *undo/redo* hingga 50 level dan rekam jejak riset di `trajectory.json`.
