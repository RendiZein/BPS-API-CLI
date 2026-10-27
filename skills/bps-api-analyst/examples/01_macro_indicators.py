#!/usr/bin/env python3
"""
Example 01: Mengambil Indikator Makroekonomi Strategis Nasional
--------------------------------------------------------------
Resep untuk menarik data ringkasan indikator makroekonomi resmi
dari BPS seperti Inflasi, PDB, Tingkat Pengangguran, dan Kemiskinan.
"""

import sys
import os

from cli_anything.bps.core.api import BPSClient


def main():
    client = BPSClient()
    print("Menghubungi BPS API untuk mengambil indikator makroekonomi...")
    
    pagination, indicators = client.get_indicators()
    print(f"Total Indikator Ditemukan: {pagination.get('total', len(indicators))}\n")

    print(f"{'Indikator':<45} | {'Nilai':<10} | {'Satuan':<15} | {'Periode'}")
    print("-" * 95)
    for ind in indicators:
        title = ind.get("title", "")
        val = ind.get("value", "")
        unit = ind.get("unit", "")
        periode = ind.get("periode", "")
        print(f"{title[:43]:<45} | {str(val):<10} | {unit[:13]:<15} | {periode}")


if __name__ == "__main__":
    main()
