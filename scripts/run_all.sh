#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source .venv/bin/activate
python src/import_excel.py
python src/scan_pdfs.py
python src/dedupe.py
python src/generate_prisma_counts.py
python src/rq_report.py
python src/export_csv.py
echo "[OK] pipeline concluído"
