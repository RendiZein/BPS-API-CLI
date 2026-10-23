#!/usr/bin/env python3
"""
Example 04: Mengambil Data Perdagangan Luar Negeri (Exim) per Kode HS
--------------------------------------------------------------------
Resep untuk menarik data ekspor atau impor komoditas Indonesia
berdasarkan kode Harmonized System (HS Code).
"""

import sys
import os

from cli_anything.bps.core.api import BPSClient


def main():
    client = BPSClient()

    # Parameter Exim:
    # sumber = 1 (Ekspor)
    # periode = 2 (Tahunan)
    # kodehs = "09" (Kopi, Teh, Mate, dan Rempah-rempah)
    # jenishs = 1 (2 digit)
    # tahun = 2023
    kodehs = "09"
    tahun = 2023

    print(f"Menarik data ekspor Indonesia untuk Kode HS [{kodehs}] tahun {tahun}...")
    items = client.get_exim(
        sumber=1,
        periode=2,
        kodehs=kodehs,
        jenishs=1,
        tahun=tahun,
    )

    print(f"Total transaksi/tujuan tercatat: {len(items)}\n")
    print(f"{'Negara Tujuan':<25} | {'Pelabuhan Muat':<25} | {'Nilai (USD)':<15} | {'Berat Bersih (Kg)'}")
    print("-" * 85)

    # Tampilkan 10 record teratas
    for item in items[:10]:
        ctr = item.get("ctr", "")
        pod = item.get("pod", "")
        val = f"{item.get('value', 0):,.2f}"
        weight = f"{item.get('netweight', 0):,}"
        print(f"{ctr[:23]:<25} | {pod[:23]:<25} | {val:<15} | {weight}")


if __name__ == "__main__":
    main()
