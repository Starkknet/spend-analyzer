# Fintech Credit Card Spend Analyzer

A polished, PM‑friendly Streamlit app that ingests credit‑card transactions and turns them into a clean dashboard, budget alerts, and a downloadable PDF report.

## ✨ Features
- **Input**: Upload a CSV/Excel with columns: `Date, Merchant, Category, Amount` (or use the provided `transactions.csv`).
- **Dashboard**: 
  - Pie chart of spend by category (per selected month)
  - Monthly spend trend line
  - Top 5 merchants by spend (per selected month)
- **Alerts & Insights**: Flags any category exceeding **30%** of the monthly **budget** (default: `$1000`, configurable).
- **Export**: One‑click **PDF** report saved under `reports/` with a timestamp and offered for download.
- **Repo Structure**
  ```
  spend-analyzer/
  ├── app.py
  ├── transactions.csv
  ├── reports/              # auto-generated reports
  ├── requirements.txt
  ├── README.md
  └── .gitignore
  ```

## 🧩 Tech Stack
- Python, **Streamlit**, **pandas**, **matplotlib**, **reportlab**

## 🚀 Run Locally
```bash
# 1) Clone your repo and enter the folder
git clone <your-repo-url>.git
cd spend-analyzer

# 2) (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Start the app
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

## 📤 Using Your Own Data
- Provide a `.csv` or `.xlsx` with columns: `Date, Merchant, Category, Amount`.
- Allowed categories (for now): `Food, Travel, Shopping, Bills, Entertainment`.

## 🧾 PDF Reports
- Click **Generate PDF report** → then **Download PDF**.
- Every report also saves automatically under `reports/SpendReport_<timestamp>.pdf`.
- Charts are embedded as images in the PDF for clear, shareable summaries.

## ☁️ Deploy (Streamlit Community Cloud)
1. Push this folder to a **public GitHub repo**.
2. Go to **streamlit.io → Deploy an app**.
3. Point to your repo, set the **main file path** to `spend-analyzer/app.py` (or root if you place files at repo root).
4. Add the **Python version** (if needed) and ensure **`requirements.txt`** is present.
5. Deploy. Your app will be available on a shareable URL.

> **Note on GitHub Pages**: GitHub Pages serves static websites only and cannot run Python apps like Streamlit. You can still host the **README** and sample **PDF reports** there, but use **Streamlit Community Cloud** (or another Python host) for the live app.

## 🤝 Contributing
- Fork the repo and create a feature branch.
- Keep PRs small, with a clear description and screenshots for UI changes.
- Style: write clean, modular Python; prefer pure `pandas` for transforms and `matplotlib` for charts.
- Add/update docstrings and README where relevant.

## ✅ PM Demo Tips
- Use the sidebar budget to show how alerts respond in real time.
- Switch months to highlight spending pattern changes.
- Export a PDF and attach it to your portfolio or LinkedIn post.

---

© 2025 Jai Aggarwal. MIT‑style licensing recommended if you plan to open‑source.\n