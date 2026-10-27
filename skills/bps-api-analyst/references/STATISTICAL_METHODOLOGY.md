# Metodologi Statistik BPS & Panduan Harmonisasi Data

Dokumen ini menjelaskan kaidah ilmiah dan karakteristik data resmi Badan Pusat Statistik (BPS) Republik Indonesia untuk analis data dan AI Agent.

---

## 1. Siklus Rilis & Frekuensi Data (Temporal Alignment)

Variabel-variabel statistik BPS memiliki siklus survei dan jadwal rilis (*Advance Release Calendar*) yang berbeda-beda:

| Indikator | Frekuensi | Periode Survei / Rilis | Catatan Metodologis |
| :--- | :--- | :--- | :--- |
| **Inflasi (IHK)** | Bulanan | Awal bulan berikutnya | Mengukur perubahan harga sekeranjang komoditas di 90+ kota IHK (Tahun Dasar 2022=100). |
| **Pertumbuhan Ekonomi (PDRB/PDB)** | Triwulanan & Tahunan | Awal Mei (Q1), Agustus (Q2), November (Q3), Februari (Q4) | Dihitung atas dasar Harga Berlaku (ADHB) dan Harga Konstan (ADHK 2010). |
| **Kemiskinan & Ketimpangan (Gini)** | Semesteran | Maret (Rilis Juli) & September (Rilis Januari) | Menggunakan data Survei Sosial Ekonomi Nasional (Susenas). Pendekatan kebutuhan dasar (*basic needs approach*). |
| **Ketenagakerjaan (TPT/TPAK)** | Semesteran | Februari (Rilis Mei) & Agustus (Rilis November) | Menggunakan data Survei Angkatan Kerja Nasional (Sakernas). |
| **Indeks Pembangunan Manusia (IPM)** | Tahunan | Rilis November/Desember | Menggunakan metode baru (UHH, HLS, RLS, Pengeluaran Riil per Kapita disesuaikan). |

### ⚠️ Aturan Harmonisasi Frekuensi:
- Jika menganalisis regresi hubungan antara **Inflasi (Bulanan)** dan **Kemiskinan (Semesteran)**, data inflasi **wajib diagregasi** (misalnya rata-rata semester I: Januari–Juni, semester II: Juli–Desember) agar selaras dengan titik waktu survei Susenas (Maret dan September).
- Jangan mencocokkan data bulanan langsung dengan data semesteran tanpa penyesuaian interpolasi atau agregasi rata-rata periode.

---

## 2. Anomali Regional & Pemekaran Wilayah (Papua 2022)

Pada akhir tahun 2022, terjadi pemekaran wilayah administratif di Pulau Papua dari **2 provinsi (34 provinsi se-Indonesia)** menjadi **6 provinsi (38 provinsi se-Indonesia)**:
- **Provinsi Induk:**
  - `9100`: Papua
  - `9200`: Papua Barat
- **Provinsi Baru (Pemekaran UU No. 14, 15, 16, 29 Tahun 2022):**
  - `9300`: Papua Selatan
  - `9400`: Papua Tengah
  - `9500`: Papua Pegunungan
  - `9600`: Papua Barat Daya

### ⚠️ Aturan Pemodelan Panel Data:
- Untuk time-series sebelum tahun 2023, data regional Papua dihitung berdasarkan 34 provinsi.
- Untuk analisis rentang panjang (misal: 2015–2025), peneliti memiliki dua opsi standar:
  1. **Opsi Agregasi Historis:** Menyatukan kembali data 4 provinsi baru ke dalam provinsi induk untuk menjaga konsistensi spasial 34 unit.
  2. **Opsi Truncation:** Membatasi analisis panel 38 provinsi hanya pada data tahun 2023 ke atas.

---

## 3. Matriks Data Dinamis & Composite Key Decoding

Data tabel dinamis BPS (`datacontent`) tidak disimpan dalam format baris-kolom konvensional, melainkan dalam bentuk kamus pasangan *key-value*:
$$\text{Composite Key} = \text{verval} + \text{var} + \text{turvar} + \text{tahun} + \text{turth}$$

- **`verval`**: ID Kategori Vertikal (misal: kode provinsi/kabupaten).
- **`var`**: ID Variabel Statistik.
- **`turvar`**: ID Turunan Variabel (0 untuk total/tanpa turunan).
- **`tahun`**: ID Tahun (misal: 126 untuk tahun tertentu).
- **`turth`**: ID Turunan Tahun / Periode (misal: semester atau bulan).

CLI `bps` telah memiliki modul dekoder otomatis (`cli_anything.bps.core.api.BPSClient.decode_composite_matrix`) yang mengubah composite key ini menjadi tabel tabular bersih (Pandas-ready / CSV-ready).
