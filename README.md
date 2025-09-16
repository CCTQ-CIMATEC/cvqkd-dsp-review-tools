# cvqkd-dsp-review-tools

Toolkit for **systematic literature review (SLR)** data management under the **APISSER methodology (Phase P6 – Tools & Data Management)**, tailored to the study of **Digital Signal Processing from Classical Coherent Systems to Continuous-Variable QKD**.

## ✨ Features
- Import screening spreadsheets (Excel/CSV) into a structured SQLite database (L-DB).
- Manage eligibility decisions, inclusion/exclusion criteria, and research question mapping.
- Link and hash local PDF files for reproducibility.
- Detect and merge duplicate records (by DOI and normalized title+year).
- Generate PRISMA-ready counts and exclusion statistics.
- Export consolidated datasets and per-RQ publication lists in CSV format.
- Fully version-controlled pipeline (Python + SQLite + Bash).

## 📂 Structure
- `src/` → Python scripts (import, scan PDFs, dedupe, reports).
- `scripts/` → Bash helpers (`setup.sh`, `run_all.sh`).
- `data/` → SQLite database (`l_db.sqlite`).
- `pdfs/` → folder for storing article PDFs.
- `exports/` → generated CSV reports and PRISMA counts.
- `Planilha_Triagem_APISSER.xlsx` → screening spreadsheet (to be provided by the user).

## 🚀 Quick start
```bash
# create environment named dsp-review with Python 3.10
conda create -n dsp-review python=3.10 -y

# activate the environment
conda activate dsp-review

# clone repository
git clone https://github.com/CCTQ-CIMATEC/cvqkd-dsp-review-tools.git
cd cvqkd-dsp-review-tools

# setup environment and DB
bash scripts/setup.sh

# run the full pipeline
bash scripts/run_all.sh
