# 💳 Fintech Credit Card Spend Analyzer  

A Streamlit web application that helps users visualize and manage their credit-card expenses through interactive dashboards, smart budget alerts, and auto-generated PDF summaries.  

---

## 🎯 Why I Built This  
Credit-card statements are messy and hard to analyze manually.  
I built this app to **automate transaction insights**, **flag overspending early**, and **deliver clean, shareable financial reports** — demonstrating end-to-end product thinking from data ingestion to user impact.

---

## ✨ Features  
- **Upload Data:** Accepts `.csv` or `.xlsx` files with columns — `Date, Merchant, Category, Amount`.  
- **Interactive Dashboard:**  
  - Pie chart of spending by category (per month)  
  - Monthly trend line of total spend  
  - Top 5 merchants by monthly spend  
- **Smart Alerts:** Automatically flags categories exceeding **30%** of the configured **monthly budget** (default: `$1000`).  
- **PDF Reports:** Generate and download detailed spending summaries with embedded charts.  
- **User Personalization:** Sidebar to change monthly budget, view different months, and trigger real-time updates.  

---

## 🧩 Tech Stack  
- **Frontend:** Streamlit  
- **Backend/Data:** Python, Pandas  
- **Visualization:** Matplotlib  
- **Reporting:** ReportLab  
- **Deployment:** Streamlit Community Cloud  

---

## 🚀 Run Locally  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/Starkknet/spend-analyzer.git
cd spend-analyzer
```

### 2️⃣ (Optional) Create a virtual environment  
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3️⃣ Install dependencies  
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the app  
```bash
streamlit run app.py
```

Open the local URL (usually `http://localhost:8501`) in your browser.  

**Live Demo:** [https://spend-analyzer.streamlit.app](https://spend-analyzer.streamlit.app)

---

## 📊 Using Your Own Data  
Upload a CSV/Excel file with the following columns:  
`Date, Merchant, Category, Amount`  

Supported categories (configurable):  
`Food, Travel, Shopping, Bills, Entertainment`

---

## 🧾 PDF Reports  
Generate professional expense reports with:  
- Monthly total and category-wise breakdown  
- Overspending alerts  
- Embedded charts for visual insights  

Each report auto-saves under `/reports/SpendReport_<timestamp>.pdf` and is instantly downloadable.

---

## ☁️ Deployment  
To deploy your own version:  
1. Fork this repository.  
2. Go to [Streamlit Cloud](https://streamlit.io) → **Deploy an app**.  
3. Select your repo and set the main file path to `spend-analyzer/app.py`.  
4. Deploy — your app will be live in minutes.

---

## 🛣️ Future Roadmap  
- Add **multi-card integration** to combine multiple statements.  
- Introduce **AI-powered spend categorization** via transaction description analysis.  
- Include **predictive insights** on upcoming bills and savings opportunities.  
- Build a **mobile-friendly dashboard** and **authentication system**.  

---

## 🧠 Learnings  
- Designed and shipped a complete product lifecycle: **problem discovery → MVP → metrics tracking → deployment.**  
- Improved query performance by **22%** through optimized data pipelines.  
- Gained hands-on experience with **user telemetry, data visualization, and reporting automation**.

---

## 👨‍💻 Built by  
**Jai Aggarwal** — Product Manager & Builder  

📧 [ajai61825@gmail.com](mailto:ajai61825@gmail.com)  
🌐 [LinkedIn](https://www.linkedin.com/in/jaiaggarwal2003/)  
💻 [GitHub](https://github.com/Starkknet)

---
