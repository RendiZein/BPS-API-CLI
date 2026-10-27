# BPS Agent-Native CLI Rules & Operational Guardrails

Aturan ini wajib ditaati oleh seluruh AI Agent (Antigravity, Cursor, Claude Code, dsb.) saat beroperasi di repositori ini atau saat plugin `bps-api-analyst` aktif.

## 1. Aturan Deterministic CLI & Output Handling
- **Selalu Gunakan `--json` Flag:** Setiap eksekusi terminal untuk binary `bps` wajib menyertakan flag `--json` (contoh: `bps status --json`, `bps audit --topic "kemiskinan" --json`).
- **Verifikasi Return Code:** Pastikan perintah menghasilkan exit code 0. Jika non-zero, tangkap payload error JSON dari `stderr` untuk analisis mitigasi otomatis.
- **Pemisahan Stream:** Jangan gabungkan `stdout` dan `stderr`. `stdout` murni diperuntukkan bagi data JSON yang valid.

## 2. Metodologi Penelitian: Probe Before Fetching
- **Dilarang Keras Langsung Fetch:** Jangan pernah memanggil `bps fetch` tanpa terlebih dahulu melakukan `bps audit` atau `bps inspect`.
- **Harmonisasi Data:** Saat menganalisis topik, evaluasi perbedaan frekuensi rilis data (bulanan, triwulanan, semesteran) dan deteksi anomali pemekaran wilayah (seperti pemekaran 38 provinsi di Papua sejak 2022).
- **Proposal Riset:** Sajikan 2-3 opsi metodologis (misal: Analisis Tren vs Regresi Panel) kepada pengguna sebelum mengekspor data massal.
- **Data Preview Protocol:** Gunakan `bps preview --var <id> --th <th_id> --json` untuk membaca `summary.json` hemat token sebelum mengeksekusi penarikan data lengkap.

## 3. Keamanan Lingkungan & Proteksi Rahasia (Strict Guardrails)
- **Isolasi API Key:** Dilarang keras membaca secara mentah atau menampilkan isi penuh `BPS_API_KEY` ke jendela chat pengguna.
- **Larangan Commit `.env`:** File `.env`, `.bps_cache.db`, `.bps_session.json`, dan `trajectory.json` tidak boleh di-stage atau di-commit ke Git.
- **Verifikasi Sebelum Push:** Sebelum commit, selalu pastikan `git status` tidak mencantumkan berkas rahasia.

## 4. Integritas Penyimpanan & Verifikasi File
- **Path Absolut:** Selalu gunakan absolute path saat memberikan argumen `--output` pada ekspor file CSV/JSON.
- **Verifikasi Fisik:** Agen wajib memverifikasi bahwa file ekspor benar-benar terbentuk di disk sebelum melaporkan keberhasilan kepada pengguna.
- **Dry-Run Safety:** Untuk dataset besar, jalankan flag `--dry-run` terlebih dahulu guna memastikan kuota request aman dari pemblokiran WAF BPS.
