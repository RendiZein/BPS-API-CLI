"""
Automated SKILL.md Generator for BPS CLI Harness.
Parses Click commands and docstrings via AST to ensure AI documentation is always 100% in sync with code.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

SKILL_TEMPLATE = """---
name: bps-api-analyst
description: Autonomous Indonesian statistical data researcher and availability auditor using official BPS Web API.
tags: [bps, statistics, economics, indonesia, data-audit]
---

# BPS Data Analyst & Auditor Skill

Gunakan skill ini ketika pengguna mengajukan pertanyaan riset ekonomi/sosial, memerlukan data statistik resmi Indonesia (BPS), atau ingin menganalisis fenomena empiris.

## 5 Golden Rules For AI Agents
1. **Always use `--json` flag** pada setiap eksekusi perintah terminal untuk mendapatkan output yang deterministik.
2. **Check return codes** (0 untuk sukses, non-zero untuk error).
3. **Parse stderr on failure:** Jika perintah gagal, tangkap objek JSON error dari `stderr` untuk memahami kode mitigasinya.
4. **Use absolute paths** untuk argumen `--output` dan verifikasi bahwa file fisik benar-benar ada di disk sebelum melapor ke pengguna.
5. **Probe Before Fetching:** Dilarang keras memanggil `fetch` sebelum menjalankan `audit` atau `inspect` dan menyajikan proposal opsi riset kepada pengguna.

## Prasyarat & Instalasi di Mesin Baru (Prerequisites)
Sebelum mengeksekusi analisis di mesin/laptop baru, pastikan kedua hal berikut:
1. **Instalasi Binary `bps`:**  
   Jika terminal merespon `'bps' is not recognized` atau `command not found`, pasang paket eksekutor Python via:
   ```bash
   pip install git+https://github.com/RendiZein/BPS-API-CLI.git
   ```
2. **Kunci API BPS Pribadi (`.env`):**  
   Pengguna wajib memiliki API Key sendiri (gratis dari https://webapi.bps.go.id/developer) dan menyimpannya di `.env`:
   ```env
   BPS_API_KEY=kunci_api_anda_di_sini
   ```

## Self-Healing & Troubleshooting (Prosedur Otomatis AI)
- **Jika Binary `bps` Belum Ada:** AI Agent harus segera menginfokan pengguna atau menawarkan diri untuk menjalankan perintah `pip install git+https://github.com/RendiZein/BPS-API-CLI.git`.
- **Jika Kunci API Hilang / Error:** Jika `bps status` mengembalikan `"key_configured": false` atau terjadi `BPSAuthError`, minta pengguna mengisi `BPS_API_KEY` di file `.env` atau mendaftar di portal resmi BPS.
- **Jika Terjadi WAF Rate Limit (HTTP 429):** CLI secara otomatis menerapkan exponential backoff. Agen cukup menunggu jeda sebelum mencoba kembali.

## Standard Operating Procedure (Alur Riset AI)
- **Langkah 0 (Readiness):** Jalankan `bps status --json` untuk memverifikasi koneksi API dan latensi server.
- **Langkah 1 (Sesi):** Identifikasi wilayah riset. Jika provinsi/kabupaten, jalankan `bps session set-domain <id>` (atau gunakan nama wilayah langsung).
- **Langkah 2 (Audit):** Jalankan `bps audit --topic "<topik>" --json` untuk memeriksa ketersediaan variabel dan rentang tahun.
- **Langkah 3 (Harmonisasi & Formulasi):** 
  - Evaluasi rentang tahun yang tersedia.
  - Periksa anomali pemekaran wilayah dan perbedaan frekuensi (bulanan vs tahunan).
  - Sajikan 2-3 proposal riset metodologis kepada pengguna (misal: Regresi Panel vs Analisis Tren).
- **Langkah 4 (Preview):** Setelah pengguna menyetujui opsi, jalankan `bps preview --var <id> --th <th_id> --json` untuk membaca `summary.json`.
- **Langkah 5 (Ekspor):** Jalankan `bps fetch --var <id> --th <th_id> --format csv --output <path>` dan berikan kesimpulan awal data.

## Command Reference

{command_table}

## Examples

### 1. Readiness Check
```bash
bps status --json
```

### 2. Audit Ketersediaan Data Topik Riset
```bash
bps audit --topic "kemiskinan" --domain "Jawa Timur" --json
```

### 3. Inspeksi Dimensi & Kategori Variabel
```bash
bps inspect --var 49 --domain 3500 --json
```

### 4. Data Preview Protocol (Summary & Head/Tail Sample)
```bash
bps preview --var 49 --th 126 --domain 3500 --json
```

### 5. Fetch & Ekspor Data ke CSV (dengan Dry-Run Safety)
```bash
# Cek kalkulasi kuota aman
bps fetch --var 49 --th 126 --domain 3500 --format csv --output data/kemiskinan_jatim_2026.csv --dry-run --json

# Eksekusi penyimpanan data riil
bps fetch --var 49 --th 126 --domain 3500 --format csv --output data/kemiskinan_jatim_2026.csv --json
```

### 6. Manajemen Sesi & Recovery Undo
```bash
bps session init --domain 3500 --name "Riset_Jatim" --json
bps session set-domain 3300 --json
bps session undo --json
```

## Progressive Disclosure: References & Recipes

Untuk rujukan metodologi atau resep skrip Python tingkat lanjut, buka dokumen spesifik di subdirektori berikut:
- [Metodologi Statistik BPS](./references/STATISTICAL_METHODOLOGY.md)
- [Cheatsheet Endpoint API](./references/BPS_API_CHEATSHEET.md)
- [Panduan Data Dinamis & Komposit](./references/dynamic_data_guide.md)
- [Blueprint Arsitektur API BPS](./references/ARCHITECTURE.md)
- [Daftar Kode Wilayah/Domain](./references/domains.md)
- [Resep Python Praktis (Examples)](./examples/)
"""


def extract_click_commands(cli_file: Path) -> List[Dict[str, str]]:
    """Parse bps_cli.py using AST to extract registered commands and docstrings."""
    commands = []
    tree = ast.parse(cli_file.read_text(encoding="utf-8"))

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            is_cmd = False
            cmd_name = node.name.replace("_cmd", "")

            for dec in node.decorator_list:
                # Matches @cli.command("name") or @session_group.command("name")
                if isinstance(dec, ast.Call):
                    if isinstance(dec.func, ast.Attribute) and dec.func.attr == "command":
                        is_cmd = True
                        if dec.args and isinstance(dec.args[0], ast.Constant):
                            cmd_name = str(dec.args[0].value)

            if is_cmd:
                doc = ast.get_docstring(node) or "No description."
                summary = doc.strip().split("\n")[0]
                commands.append({"command": cmd_name, "description": summary})

    return commands


def generate_skill_markdown(output_path: Path, cli_file: Path) -> None:
    """Generate canonical SKILL.md from AST command extraction."""
    commands = extract_click_commands(cli_file)
    table_rows = ["| Command | Description |", "| :--- | :--- |"]
    for c in commands:
        table_rows.append(f"| `bps {c['command']}` | {c['description']} |")

    command_table = "\n".join(table_rows)
    content = SKILL_TEMPLATE.replace("{command_table}", command_table)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8", newline="\n")
    print(f"Generated SKILL.md with {len(commands)} commands at {output_path}")


if __name__ == "__main__":
    cli_path = Path("cli_anything/bps/bps_cli.py")
    target_skill = Path("skills/bps-api-analyst/SKILL.md")
    generate_skill_markdown(target_skill, cli_path)
