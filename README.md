# Utility Belt

Small, focused utilities (Python package + example notebooks). Ready for OSS use.

## What’s inside

- `src/utility_belt/` — reusable code:
  - `files/merge.py` — merge text-friendly files into one TXT
  - `web/minimal_html.py` — scrape + produce minimal HTML (from your upload)
  - `text/remove_emojis.py` — text cleaning helpers (from your upload)
  - `pdf/write_string_report_to_pdf.py` — simple PDF report writer (from your upload)
  - `storage/in_memory_database.py` — in-memory store (from your upload)
- `notebooks/` — example workflows:
  - `merge-files-to-text.ipynb` (cleaned & documented)
  - `extract-minimal-html.ipynb`
  - `extract-data-from-pdfs.ipynb`
  - `bulk-rename-files.ipynb`
  - `open-url-print-to-pdf.ipynb`
  - `text-processing.ipynb`
  - `convert-txt-to-table.ipynb`

## Quick start

```bash
# optional but recommended
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -e .[dev]
# run the CLI
ub-merge-files --input-dir . --output merged_output.txt
```

## Development

- Pre-commit hooks: `nbstripout`, `ruff`, `black`, EOF fixer
- Linting: `ruff`, `black`
- Tests: `pytest`

## License
MIT (see `LICENSE`)
