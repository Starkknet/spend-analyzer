
import os
import io
from datetime import datetime
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

# ---------- CONFIG ----------
st.set_page_config(page_title="Credit Card Spend Analyzer", layout="wide")
REPORTS_DIR = "reports"
SAMPLE_PATH = "transactions.csv"
DEFAULT_BUDGET = 1000.0  # USD

ALLOWED_CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Entertainment"]

# Ensure reports dir exists
os.makedirs(REPORTS_DIR, exist_ok=True)


# ---------- HELPERS ----------
def load_data(upload):
    if upload is not None:
        df = pd.read_csv(upload) if upload.name.endswith(".csv") else pd.read_excel(upload)
    else:
        if os.path.exists(SAMPLE_PATH):
            df = pd.read_csv(SAMPLE_PATH)
        else:
            st.error("No data provided and sample 'transactions.csv' not found.")
            st.stop()

    # Clean columns
    expected = ["Date", "Merchant", "Category", "Amount"]
    missing = [c for c in expected if c not in df.columns]
    if missing:
        st.error(f"Missing columns: {', '.join(missing)}")
        st.stop()

    # Parse and validate
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Category"] = df["Category"].astype(str)

    df = df.dropna(subset=["Date", "Amount"])
    return df


def money(x, pos):
    return f"${x:,.0f}"


def build_charts(df_month, df_all):
    """Return file paths of saved charts and also display them inline."""

    chart_paths = {}

    # ----- Pie: spend by category (current month) -----
    cat_sum = df_month.groupby("Category")["Amount"].sum().reindex(ALLOWED_CATEGORIES, fill_value=0)
    fig1, ax1 = plt.subplots(figsize=(5.5, 5.5))
    non_zero = cat_sum[cat_sum > 0]
    if non_zero.empty:
        labels = ["No spend"]
        values = [1]
    else:
        labels = list(non_zero.index)
        values = list(non_zero.values)
    ax1.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    ax1.set_title("Spend by Category (This Month)")
    st.pyplot(fig1, use_container_width=False)
    pie_path = os.path.join(REPORTS_DIR, "pie.png")
    fig1.savefig(pie_path, bbox_inches="tight", dpi=180)
    plt.close(fig1)
    chart_paths["pie"] = pie_path

    # ----- Trend: monthly spend over time -----
    df_all = df_all.copy()
    df_all["Month"] = df_all["Date"].dt.to_period("M").dt.to_timestamp()
    trend = df_all.groupby("Month")["Amount"].sum().reset_index()
    fig2, ax2 = plt.subplots(figsize=(7, 4.5))
    ax2.plot(trend["Month"], trend["Amount"], marker="o")
    ax2.set_title("Monthly Spend Trend")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Spend")
    ax2.yaxis.set_major_formatter(FuncFormatter(money))
    ax2.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig2, use_container_width=True)
    trend_path = os.path.join(REPORTS_DIR, "trend.png")
    fig2.savefig(trend_path, bbox_inches="tight", dpi=180)
    plt.close(fig2)
    chart_paths["trend"] = trend_path

    # ----- Top 5 merchants (current month) -----
    merch = df_month.groupby("Merchant")["Amount"].sum().sort_values(ascending=False).head(5)
    fig3, ax3 = plt.subplots(figsize=(7, 4.5))
    merch.plot(kind="bar", ax=ax3)
    ax3.set_title("Top 5 Merchants by Spend (This Month)")
    ax3.set_xlabel("Merchant")
    ax3.set_ylabel("Spend")
    ax3.yaxis.set_major_formatter(FuncFormatter(money))
    ax3.grid(axis="y", linestyle="--", alpha=0.4)
    st.pyplot(fig3, use_container_width=True)
    merch_path = os.path.join(REPORTS_DIR, "merchants.png")
    fig3.savefig(merch_path, bbox_inches="tight", dpi=180)
    plt.close(fig3)
    chart_paths["merchants"] = merch_path

    return chart_paths


def generate_insights(df_month, budget):
    total = df_month["Amount"].sum()
    insights = []
    if total <= 0:
        return ["No transactions this month."], {}

    by_cat = df_month.groupby("Category")["Amount"].sum().reindex(ALLOWED_CATEGORIES, fill_value=0)

    for cat, amt in by_cat.items():
        pct = (amt / budget) * 100.0 if budget > 0 else 0.0
        if pct > 30.0:
            insights.append(f"⚠️ You spent {pct:.0f}% of your budget on {cat} this month.")
        else:
            insights.append(f"✅ {cat} is within safe range ({pct:.0f}%).")

    context = {
        "total_spend": total,
        "by_cat": by_cat.to_dict(),
    }
    return insights, context


def split_long_text(text, max_chars):
    out, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 <= max_chars:
            cur = (cur + " " + word).strip()
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def export_pdf(charts, insights, budget, month_label):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(REPORTS_DIR, f"SpendReport_{ts}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    margin = 1.2 * cm

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin, height - margin, "Credit Card Spend Analyzer — Report")

    # Subtitle / meta
    c.setFont("Helvetica", 10)
    c.drawString(margin, height - margin - 14, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(margin, height - margin - 28, f"Month: {month_label}   |   Budget: ${budget:,.0f}")

    # Insights block
    y = height - margin - 50
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Alerts & Insights")
    y -= 14
    c.setFont("Helvetica", 10)
    for ins in insights:
        for line in split_long_text(ins, 95):
            c.drawString(margin, y, f"• {line}")
            y -= 12
            if y < 6 * cm:
                c.showPage()
                y = height - margin
                c.setFont("Helvetica", 10)

    # Insert charts, each on its own space
    def draw_image(img_path, caption):
        nonlocal y
        if not os.path.exists(img_path):
            return
        if y < 12 * cm:
            c.showPage()
            y = height - margin
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin, y, caption)
        y -= 10
        img = ImageReader(img_path)
        img_w, img_h = img.getSize()
        max_w = width - 2 * margin
        scale = min(max_w / img_w, 9 * cm / img_h)
        c.drawImage(img, margin, y - img_h * scale, width=img_w * scale, height=img_h * scale)
        y -= img_h * scale + 12

    draw_image(charts.get("pie", ""), "Spend by Category (This Month)")
    draw_image(charts.get("trend", ""), "Monthly Spend Trend")
    draw_image(charts.get("merchants", ""), "Top 5 Merchants by Spend (This Month)")

    c.showPage()
    c.save()
    return pdf_path


# ---------- UI ----------
st.title("💳 Fintech Credit Card Spend Analyzer")
with st.sidebar:
    st.header("Controls")
    uploaded = st.file_uploader("Upload transactions (.csv or .xlsx)", type=["csv", "xlsx"])
    budget = st.number_input("Monthly budget (USD)", min_value=100.0, value=DEFAULT_BUDGET, step=50.0)
    st.markdown("---")
    st.write("**Tips**")
    st.write("• Use the sample CSV if you don't have data.")
    st.write("• Adjust the budget and re-generate the report.")

# Data
df = load_data(uploaded)
df = df[df["Category"].isin(ALLOWED_CATEGORIES)]
if df.empty:
    st.warning("No rows after filtering to allowed categories.")
    st.stop()

# Month selection defaults to the latest month in the file
df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)
latest_month = sorted(df["YearMonth"].unique())[-1]
month_choice = st.selectbox("Select month", options=sorted(df["YearMonth"].unique()), index=sorted(df["YearMonth"].unique()).index(latest_month))

df_month = df[df["YearMonth"] == month_choice].copy()

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    total_spend = df_month["Amount"].sum()
    st.metric("Total Spend (Selected Month)", f"${total_spend:,.0f}")
with col2:
    txn_count = len(df_month)
    st.metric("Transactions", f"{txn_count}")
with col3:
    avg_txn = df_month["Amount"].mean() if txn_count > 0 else 0.0
    st.metric("Avg. Transaction", f"${avg_txn:,.0f}")

# Charts
st.markdown("### 📊 Dashboard")
charts = build_charts(df_month, df)

# Alerts & Insights
st.markdown("### 🔔 Alerts & Insights")
insights, ctx = generate_insights(df_month, budget)
for ins in insights:
    if ins.startswith("⚠️"):
        st.warning(ins)
    else:
        st.success(ins)

# Export Button
st.markdown("### 🧾 Export Report")
month_label = month_choice
if st.button("Generate PDF report"):
    pdf_path = export_pdf(charts, insights, budget, month_label)
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="Download PDF",
            data=f.read(),
            file_name=os.path.basename(pdf_path),
            mime="application/pdf"
        )
    st.info(f"Report saved to: {pdf_path}")
