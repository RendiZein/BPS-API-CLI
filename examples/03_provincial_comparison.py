#!/usr/bin/env python3
"""
Example 03: Membandingkan Indikator Lintas Provinsi (Regional Comparison)
-----------------------------------------------------------------------
Resep untuk menarik dan membandingkan data indikator makroekonomi
dari beberapa domain provinsi di Indonesia.
"""

import sys
import os

from cli_anything.bps.core.api import BPSClient


def main():
    client = BPSClient()

    # Domain yang dibandingkan:
    # 0000 = Nasional, 3100 = DKI Jakarta, 3200 = Jawa Barat, 3500 = Jawa Timur, 5100 = Bali
    targets = [
        ("0000", "Nasional / Pusat"),
        ("3100", "DKI Jakarta"),
        ("3200", "Jawa Barat"),
        ("3500", "Jawa Timur"),
        ("5100", "Bali"),
    ]

    print("Mengumpulkan indikator makroekonomi untuk beberapa wilayah...\n")
    print(f"{'Wilayah':<20} | {'Pertumbuhan Ekonomi':<25} | {'Inflasi YoY':<20} | {'Penduduk Miskin'}")
    print("-" * 85)

    for domain_id, domain_name in targets:
        try:
            _, indicators = client.get_indicators(domain=domain_id)
            
            # Cari nilai indikator utama
            gdp = "-"
            inflasi = "-"
            miskin = "-"

            for ind in indicators:
                title = ind.get("title", "").lower()
                val = str(ind.get("value", "-"))
                unit = ind.get("unit", "")
                
                if "pertumbuhan ekonomi" in title and gdp == "-":
                    gdp = f"{val} {unit}"
                elif "inflasi year on year" in title and inflasi == "-":
                    inflasi = f"{val} {unit}"
                elif "penduduk miskin" in title and miskin == "-":
                    miskin = f"{val} {unit}"

            print(f"{domain_name:<20} | {gdp:<25} | {inflasi:<20} | {miskin}")
        except Exception as e:
            print(f"{domain_name:<20} | Error: {e}")


if __name__ == "__main__":
    main()
