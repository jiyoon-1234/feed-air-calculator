# Feed Air Calculator

Feed composition and flow calculator for theoretical air demand.

## Features

- Upload `.xlsx`, `.csv`, `.tsv`, and text-based `.pdf` tables.
- Parse ordinary component flow tables.
- Parse process stream tables with `Mass Flowrate`, `Molecular Weight`, and `Component (mole%)`.
- Calculate molecular weight from chemical formulas when MW is missing.
- Calculate net oxygen demand and theoretical air flow.
- Export results as CSV.

## Local Run

```powershell
python app.py
```

Open:

```text
http://localhost:8766/
```

If port `8766` is busy, the app automatically tries the next available port.

## Deploy With Render

1. Push this project to GitHub.
2. Go to Render and create a new Web Service.
3. Connect the GitHub repository.
4. Use these settings:

```text
Build Command: pip install -r requirements.txt
Start Command: python app.py --no-browser
```

Render also detects `render.yaml`, so the settings can be applied automatically.

## Notes

- GitHub Pages cannot run the Python upload parser, so use Render, Railway, Fly.io, or another Python web service host.
- Scanned PDF files need OCR before upload. Text-based PDFs can be parsed.
- Legacy `.xls` files should be saved as `.xlsx` or `.csv`.
