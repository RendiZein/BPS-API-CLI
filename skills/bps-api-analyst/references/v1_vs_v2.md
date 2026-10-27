# Analisis Komparasi BPS API V1 vs V2

Dokumen ini mencatat temuan teknis mengenai versi API yang ada di server Badan Pusat Statistik (`webapi.bps.go.id`).

---

## 1. Status Versi di Server BPS

Pengecekan langsung (*live probe*) ke server BPS menunjukkan adanya dua versi mesin API:

| Endpoint Root | Status HTTP | Respons JSON | Status Operasional |
| :--- | :--- | :--- | :--- |
| `GET https://webapi.bps.go.id/v1/` | `200 OK` | `{"title":"API Badan Pusat Statistik","version":"1.0.0"}` | **Production Aktif (Digunakan saat ini)** |
| `GET https://webapi.bps.go.id/v2/` | `200 OK` | `{"title":"API Badan Pusat Statistik V2","version":"2.0.0"}` | **Restricted / Pre-release Engine** |
| `GET https://webapi.bps.go.id/v3/` | `404 Not Found` | `<!DOCTYPE HTML... 404 Not Found>` | Tidak ada |

---

## 2. Struktur Endpoint & Controller

Kedua versi dibangun menggunakan framework PHP (Yii2) dan memiliki daftar controller/action yang identik:

* `.../api/domain`
* `.../api/list`
* `.../api/view`
* `.../api/interoperabilitas`
* `.../api/dataexim`

Format rute parameter pada kedua versi juga sama (path segments):
`/api/list/model/{model}/domain/{domain}/key/{key}/...`

---

## 3. Perbedaan Teknis Utama

### A. Kode Status HTTP saat Kegagalan Autentikasi
* **V1**: Mengembalikan **HTTP 200 OK** meskipun API Key salah atau tidak terdaftar.
  ```json
  {"status": "Error", "message": "You are not Allowed to take this action. Please re-check your key"}
  ```
* **V2**: Mengikuti standar REST RFC dengan mengembalikan **HTTP 401 Unauthorized**.
  ```json
  {"status": "Error", "message": "You are not authorized to access this page. ERRAUTH002"}
  ```

### B. Otorisasi API Key Publik
* **V1**: Kunci pengembang publik (yang diperoleh dari `webapi.bps.go.id/developer`) berstatus **aktif dan diotorisasi penuh** untuk seluruh endpoint data statistik, sensus, dan publikasi.
* **V2**: Kunci pengembang publik ditolak dengan kode galat **`ERRAUTH002`**.
  * `ERRAUTH002` mengindikasikan bahwa token/kunci belum diprovisi atau tidak memiliki hak akses (*permission scope*) untuk lingkungan V2.
  * Lingkungan V2 kemungkinan besar dialokasikan untuk instansi pemerintah (Satu Data Indonesia / SDI) atau memerlukan permohonan persetujuan khusus ke administrator BPS.

### C. Dokumentasi Resmi
* Seluruh portal resmi (`https://webapi.bps.go.id/developer` dan `https://webapi.bps.go.id/documentation`) per saat ini secara eksklusif mendokumentasikan dan mereferensikan endpoint **`/v1/`**.
* Tidak ada dokumentasi publik untuk `/v2/`.

---

## 4. Konfigurasi Transisi (Future-Proofing)

Skill BPS API ini dirancang fleksibel:
1. Secara default, skill menggunakan **`v1`** (`https://webapi.bps.go.id/v1/api`).
2. Jika di masa mendatang BPS mengaktifkan API Key Anda untuk V2 atau merilis V2 ke publik, Anda cukup mengubah konfigurasi di `.env`:
   ```env
   BPS_API_VERSION=v2
   ```
3. Tidak diperlukan perubahan kode logika pemanggil karena struktur parameter dan aksi endpoint di V2 identik dengan V1.
