#!/usr/bin/env python3
"""
Example 02: Menarik Data Dinamis dan Menyimpan ke File CSV
---------------------------------------------------------
Resep untuk menarik data multi-dimensi statistik (Dynamic Data),
mendekode kunci komposit, dan mengekspor hasilnya langsung ke CSV.
"""

import sys
import os
import csv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from bps_client import BPSClient


def main():
    client = BPSClient()

    # Variabel: 1753 (Nilai Ekspor Migas - Non Migas)
    var_id = 1753

    # Langkah 1: Cek ketersediaan periode th
    print(f"Mencari periode data yang tersedia untuk var_id {var_id}...")
    _, periods = client.get_periods(var_id=var_id)
    if not periods:
        print("Periode tidak ditemukan.")
        return

    latest_th = periods[0]
    th_id = latest_th.get("th_id")
    th_label = latest_th.get("th")
    print(f"Menggunakan periode terbaru: {th_label} (ID: {th_id})\n")

    # Langkah 2: Ambil raw dynamic data
    print("Mengunduh data dinamis dari BPS API...")
    raw_data = client.get_dynamic_data(var_id=var_id, th_id=th_id)

    # Langkah 3: Dekode kunci komposit ke record datar
    print("Mendekode kunci komposit datacontent...")
    decoded_rows = client.decode_dynamic_data(raw_data)
    print(f"Berhasil mendekode {len(decoded_rows)} baris data.\n")

    # Langkah 4: Tulis ke file CSV
    out_file = "ekspor_migas_decoded.csv"
    if decoded_rows:
        headers = [h for h in decoded_rows[0].keys() if not h.startswith("_")]
        with open(out_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(decoded_rows)
        print(f"File berhasil disimpan ke: {out_file}")

        # Tampilkan 5 baris pertama di terminal
        print("\nContoh 5 baris pertama:")
        for r in decoded_rows[:5]:
            print(f"- {r.get('Komponen Ekspor Impor', '')} | {r.get('Periode', '')} {r.get('Tahun', '')}: {r.get('Nilai', '')} {r.get('Satuan', '')}")

    # Bersihkan file output contoh setelah verifikasi
    if os.path.exists(out_file):
        os.remove(out_file)
        print(f"(File {out_file} telah dibersihkan)")


if __name__ == "__main__":
    main()
