# 🛒 LuLu UAE Retail Intelligence Dashboard

An executive-grade Streamlit dashboard providing actionable insights into LuLu Hypermarket's retail performance across the UAE.

## 📊 Dashboard Features

### KPI Cards
- Total Revenue, Orders, Units Sold, Avg Basket Size, Promo Usage Rate, Return Rate

### Tab 1 · Sales Trends
- Monthly revenue & quantity trend (dual-axis)
- Order volume by month
- Revenue by department (color = units sold)
- Order volume by day of week
- Shopping hour heatmap (day × hour)

### Tab 2 · City & Zone Performance
- Revenue ranking by city
- Orders vs Avg Order Value scatter (bubble = units)
- Top 15 zones by revenue
- City × Department revenue heatmap

### Tab 3 · Promo Analysis
- Promo vs No-Promo: avg revenue, avg units, transaction split
- Revenue & order count by promo code type
- Promo type adoption heatmap by city

### Tab 4 · Payment Insights
- Transaction share by payment method (donut)
- Avg order value by payment method
- Payment method mix by city (stacked bar)
- Payment method trend over time (line)
- Digital vs traditional adoption area chart

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app**
4. Select your repo, branch `main`, file `app.py`
5. Click **Deploy**

## 📁 Data

The dashboard reads `lulu_uae_master_2000.csv` from the same directory.  
Dataset: LuLu UAE transactional retail data · Apr–Oct 2025 · 2,000 records · 35 fields.

## 🛠️ Tech Stack

- **Streamlit** — dashboard framework
- **Plotly** — interactive charts
- **Pandas** — data processing
