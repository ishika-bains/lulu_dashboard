import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LuLu UAE · Retail Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0e1a 0%, #111827 100%);
    border-right: 1px solid #1e2a3a;
  }
  [data-testid="stSidebar"] * { color: #c9d4e8 !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stMultiSelect label { color: #7e95bb !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 0.08em; }

  /* Main background */
  .main { background-color: #080c14; }
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px; }

  /* Metric cards */
  .kpi-card {
    background: linear-gradient(135deg, #0f1729 0%, #141e33 100%);
    border: 1px solid #1e2d47;
    border-radius: 14px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
  }
  .kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, #3b82f6);
  }
  .kpi-label {
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #5a7499;
    margin-bottom: 8px;
  }
  .kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #e8edf8;
    line-height: 1;
  }
  .kpi-delta {
    font-size: 12px;
    margin-top: 6px;
    color: #4ade80;
  }
  .kpi-icon {
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 36px;
    opacity: 0.15;
  }

  /* Section headers */
  .section-header {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #c8d5ec;
    letter-spacing: 0.02em;
    padding: 8px 0 4px 0;
    border-bottom: 1px solid #1e2d47;
    margin-bottom: 16px;
  }
  .section-sub {
    font-size: 12px;
    color: #4a6080;
    margin-top: -12px;
    margin-bottom: 16px;
  }

  /* Chart containers */
  .chart-box {
    background: #0f1729;
    border: 1px solid #1a2540;
    border-radius: 14px;
    padding: 18px;
  }

  /* Plotly overrides */
  .js-plotly-plot .plotly { background: transparent !important; }

  /* Hide Streamlit chrome */
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
  header {visibility: hidden;}

  /* Tab styling */
  .stTabs [data-baseweb="tab-list"] {
    background: #0a0e1a;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #5a7499;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    font-weight: 500;
  }
  .stTabs [aria-selected="true"] {
    background: #1a2d50 !important;
    color: #93c5fd !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("lulu_uae_master_2000.csv")
    df["order_datetime"] = pd.to_datetime(df["order_datetime"])
    df["order_month_dt"] = pd.to_datetime(df["order_month"])
    return df

df_full = load_data()

# ─── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 16px 0 24px 0;'>
      <div style='font-family: Syne, sans-serif; font-size: 22px; font-weight: 800; color: #e2ebff; letter-spacing: -0.01em;'>🛒 LuLu UAE</div>
      <div style='font-size: 11px; color: #3d5475; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 2px;'>Retail Intelligence Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    all_cities = sorted(df_full["city"].unique())
    sel_cities = st.multiselect("City", all_cities, default=all_cities, key="cities")

    all_months = sorted(df_full["order_month"].unique())
    sel_months = st.multiselect("Month", all_months, default=all_months, key="months")

    all_depts = sorted(df_full["department"].unique())
    sel_depts = st.multiselect("Department", all_depts, default=all_depts, key="depts")

    all_pay = sorted(df_full["payment_method"].unique())
    sel_pay = st.multiselect("Payment Method", all_pay, default=all_pay, key="pay")

    st.markdown("---")
    st.markdown("<div style='font-size:11px; color:#2d4060;'>Data: LuLu UAE Transactions 2025</div>", unsafe_allow_html=True)

# ─── Filter data ───────────────────────────────────────────────────────────────
df = df_full[
    df_full["city"].isin(sel_cities) &
    df_full["order_month"].isin(sel_months) &
    df_full["department"].isin(sel_depts) &
    df_full["payment_method"].isin(sel_pay)
].copy()

# ─── Plotly Template ───────────────────────────────────────────────────────────
TEMPLATE = dict(
    layout=go.Layout(
        font=dict(family="DM Sans", color="#8aa3c4"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=["#3b82f6", "#f59e0b", "#10b981", "#a78bfa", "#f43f5e", "#06b6d4"],
        xaxis=dict(gridcolor="#1a2540", zerolinecolor="#1a2540", tickfont=dict(color="#5a7499")),
        yaxis=dict(gridcolor="#1a2540", zerolinecolor="#1a2540", tickfont=dict(color="#5a7499")),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=30, b=10),
    )
)

COLORS = {
    "blue": "#3b82f6",
    "amber": "#f59e0b",
    "green": "#10b981",
    "purple": "#a78bfa",
    "rose": "#f43f5e",
    "cyan": "#06b6d4",
    "slate": "#64748b",
}

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom: 24px;'>
  <div style='font-family: Syne, sans-serif; font-size: 28px; font-weight: 800; color: #dce8ff; letter-spacing: -0.02em;'>
    Retail Performance Dashboard
  </div>
  <div style='font-size: 13px; color: #3d5475; margin-top: 4px;'>
    LuLu Hypermarket · UAE Operations · Apr – Oct 2025
  </div>
</div>
""", unsafe_allow_html=True)

# ─── KPI Cards ─────────────────────────────────────────────────────────────────
total_revenue = df["line_value_aed"].sum()
total_orders = df["order_id"].nunique()
total_qty = df["quantity"].sum()
avg_basket = df["basket_size_items"].mean()
promo_rate = df["promo_used"].mean() * 100
return_rate = df["returned"].mean() * 100

col1, col2, col3, col4, col5, col6 = st.columns(6)

kpis = [
    (col1, "Total Revenue", f"AED {total_revenue/1e6:.2f}M", "#3b82f6", "💰"),
    (col2, "Total Orders", f"{total_orders:,}", "#10b981", "📦"),
    (col3, "Units Sold", f"{total_qty:,}", "#f59e0b", "🏷️"),
    (col4, "Avg Basket Size", f"{avg_basket:.1f} items", "#a78bfa", "🛒"),
    (col5, "Promo Usage", f"{promo_rate:.1f}%", "#06b6d4", "🎟️"),
    (col6, "Return Rate", f"{return_rate:.1f}%", "#f43f5e", "↩️"),
]

for col, label, value, color, icon in kpis:
    with col:
        st.markdown(f"""
        <div class='kpi-card' style='--accent: {color};'>
          <div class='kpi-label'>{label}</div>
          <div class='kpi-value'>{value}</div>
          <div class='kpi-icon'>{icon}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📈 Sales Trends", "🗺️ City & Zone", "🎟️ Promo Analysis", "💳 Payment Insights"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 · SALES TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<div class='section-header'>Monthly Sales Trends</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Revenue and quantity movements across the dataset period</div>", unsafe_allow_html=True)

    monthly = df.groupby("order_month").agg(
        Revenue=("line_value_aed", "sum"),
        Quantity=("quantity", "sum"),
        Orders=("order_id", "count")
    ).reset_index().sort_values("order_month")
    monthly["Month Label"] = monthly["order_month"].str.replace("2025-", "", regex=False)

    c1, c2 = st.columns([3, 2])

    with c1:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=monthly["Month Label"], y=monthly["Revenue"],
            name="Revenue (AED)", marker_color=COLORS["blue"],
            marker_opacity=0.85, marker_cornerradius=4,
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=monthly["Month Label"], y=monthly["Quantity"],
            name="Units Sold", mode="lines+markers",
            line=dict(color=COLORS["amber"], width=2.5),
            marker=dict(size=7, color=COLORS["amber"]),
        ), secondary_y=True)
        fig.update_layout(height=300, title_text="Revenue vs Units Sold by Month")
        fig.update_yaxes(title_text="Revenue (AED)", secondary_y=False, tickformat=",.0f")
        fig.update_yaxes(title_text="Units Sold", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.bar(
            monthly, x="Orders", y="Month Label", orientation="h",
            title="Order Volume by Month",
            color="Orders",
            color_continuous_scale=["#0f1e3d", "#3b82f6"],
        )
        fig2.update_layout(height=300, coloraxis_showscale=False)
        fig2.update_traces(marker_cornerradius=4)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='section-header' style='margin-top:20px;'>Department & Day-of-Week Breakdown</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)

    with c3:
        dept = df.groupby("department").agg(
            Revenue=("line_value_aed", "sum"),
            Quantity=("quantity", "sum")
        ).reset_index().sort_values("Revenue", ascending=True)
        fig3 = px.bar(dept, x="Revenue", y="department", orientation="h",
                      color="Quantity", color_continuous_scale=["#0f1e3d", "#f59e0b"],
                      title="Revenue by Department (color = Units)")
        fig2.update_layout(height=300, coloraxis_showscale=False)
        fig3.update_coloraxes(colorbar=dict(thickness=8, len=0.6, tickfont=dict(color="#5a7499")))
        fig3.update_traces(marker_cornerradius=4)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow = df.groupby("day_of_week").agg(Orders=("order_id", "count")).reset_index()
        dow["day_of_week"] = pd.Categorical(dow["day_of_week"], categories=day_order, ordered=True)
        dow = dow.sort_values("day_of_week")
        fig4 = px.bar(dow, x="day_of_week", y="Orders", title="Order Volume by Day of Week",
                      color="Orders", color_continuous_scale=["#0f1e3d", "#10b981"])
        fig4.update_layout(**TEMPLATE["layout"], height=320, coloraxis_showscale=False)
        fig4.update_traces(marker_cornerradius=4)
        st.plotly_chart(fig4, use_container_width=True)

    # Hour heatmap
    st.markdown("<div class='section-header' style='margin-top:20px;'>Shopping Hour Heatmap</div>", unsafe_allow_html=True)
    hour_day = df.groupby(["day_of_week", "hour_of_day"]).agg(Orders=("order_id", "count")).reset_index()
    hour_pivot = hour_day.pivot_table(index="day_of_week", columns="hour_of_day", values="Orders", fill_value=0)
    hour_pivot = hour_pivot.reindex([d for d in day_order if d in hour_pivot.index])
    fig5 = go.Figure(go.Heatmap(
        z=hour_pivot.values, x=hour_pivot.columns.astype(str), y=hour_pivot.index,
        colorscale=[[0, "#080c14"], [0.3, "#0f2040"], [0.7, "#1d4d8c"], [1, "#3b82f6"]],
        showscale=True, colorbar=dict(thickness=8, tickfont=dict(color="#5a7499")),
        hovertemplate="Day: %{y}<br>Hour: %{x}:00<br>Orders: %{z}<extra></extra>"
    ))
    fig5.update_layout(**TEMPLATE["layout"], height=260, title_text="Peak Shopping Hours")
    fig5.update_xaxes(title="Hour of Day")
    st.plotly_chart(fig5, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 · CITY & ZONE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-header'>City Performance Overview</div>", unsafe_allow_html=True)

    city_df = df.groupby("city").agg(
        Revenue=("line_value_aed", "sum"),
        Quantity=("quantity", "sum"),
        Orders=("order_id", "count"),
        Avg_Order_Value=("line_value_aed", "mean")
    ).reset_index().sort_values("Revenue", ascending=False)

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            city_df.sort_values("Revenue"), x="Revenue", y="city",
            orientation="h", title="Total Revenue by City",
            color="Revenue", color_continuous_scale=["#0d1e3a", "#3b82f6"],
            text="Revenue"
        )
        fig.update_traces(texttemplate="AED %{text:,.0f}", textposition="outside",
                          textfont=dict(color="#5a7499", size=10), marker_cornerradius=4)
        fig.update_layout(**TEMPLATE["layout"], height=350, coloraxis_showscale=False,
                          xaxis=dict(showticklabels=False, showgrid=False))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.scatter(
            city_df, x="Orders", y="Avg_Order_Value",
            size="Quantity", color="city", text="city",
            title="Orders vs Avg Order Value (bubble = units sold)",
            color_discrete_sequence=["#3b82f6", "#f59e0b", "#10b981", "#a78bfa", "#f43f5e", "#06b6d4", "#fbbf24", "#34d399"]
        )
        fig2.update_traces(textposition="top center", textfont=dict(size=9))
        fig2.update_layout(**TEMPLATE["layout"], height=350, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='section-header' style='margin-top:20px;'>Zone Performance</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Top 15 zones by total revenue</div>", unsafe_allow_html=True)

    zone_df = df.groupby(["city", "city_zone"]).agg(
        Revenue=("line_value_aed", "sum"),
        Quantity=("quantity", "sum"),
        Orders=("order_id", "count")
    ).reset_index().sort_values("Revenue", ascending=False).head(15)
    zone_df["Zone Label"] = zone_df["city_zone"] + " (" + zone_df["city"] + ")"

    fig3 = px.bar(
        zone_df.sort_values("Revenue"), x="Revenue", y="Zone Label",
        orientation="h", title="Top 15 Zones by Revenue",
        color="city",
        color_discrete_sequence=["#3b82f6", "#f59e0b", "#10b981", "#a78bfa", "#f43f5e", "#06b6d4", "#fbbf24", "#34d399"]
    )
    fig3.update_layout(**TEMPLATE["layout"], height=430)
    fig3.update_traces(marker_cornerradius=4)
    st.plotly_chart(fig3, use_container_width=True)

    # City × Dept heatmap
    st.markdown("<div class='section-header' style='margin-top:20px;'>City × Department Revenue Matrix</div>", unsafe_allow_html=True)
    cd = df.groupby(["city", "department"])["line_value_aed"].sum().reset_index()
    cd_pivot = cd.pivot_table(index="city", columns="department", values="line_value_aed", fill_value=0)
    fig4 = go.Figure(go.Heatmap(
        z=cd_pivot.values,
        x=cd_pivot.columns,
        y=cd_pivot.index,
        colorscale=[[0, "#080c14"], [0.4, "#0f2f5a"], [1, "#3b82f6"]],
        showscale=True,
        colorbar=dict(thickness=8, tickformat=",.0f", tickfont=dict(color="#5a7499")),
        hovertemplate="City: %{y}<br>Dept: %{x}<br>Revenue: AED %{z:,.0f}<extra></extra>",
        text=[[f"AED {v:,.0f}" for v in row] for row in cd_pivot.values],
        texttemplate="%{text}", textfont=dict(size=9, color="#7090b0"),
    ))
    fig4.update_layout(**TEMPLATE["layout"], height=320, title_text="Revenue Heatmap: City × Department")
    st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 · PROMO ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-header'>Promo Code Effectiveness</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    promo_effect = df.groupby("promo_used").agg(
        Avg_Revenue=("line_value_aed", "mean"),
        Avg_Qty=("quantity", "mean"),
        Count=("order_id", "count")
    ).reset_index()
    promo_effect["Label"] = promo_effect["promo_used"].map({0: "No Promo", 1: "With Promo"})

    with c1:
        fig = px.bar(promo_effect, x="Label", y="Avg_Revenue",
                     title="Avg Revenue: Promo vs No Promo",
                     color="Label",
                     color_discrete_map={"No Promo": "#334155", "With Promo": "#3b82f6"})
        fig.update_layout(**TEMPLATE["layout"], height=280, showlegend=False)
        fig.update_traces(marker_cornerradius=6)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.bar(promo_effect, x="Label", y="Avg_Qty",
                      title="Avg Units per Order",
                      color="Label",
                      color_discrete_map={"No Promo": "#334155", "With Promo": "#f59e0b"})
        fig2.update_layout(**TEMPLATE["layout"], height=280, showlegend=False)
        fig2.update_traces(marker_cornerradius=6)
        st.plotly_chart(fig2, use_container_width=True)

    with c3:
        fig3 = px.pie(promo_effect, values="Count", names="Label",
                      title="Transaction Split",
                      color="Label",
                      color_discrete_map={"No Promo": "#1e2d47", "With Promo": "#3b82f6"},
                      hole=0.55)
        fig3.update_layout(**TEMPLATE["layout"], height=280)
        fig3.update_traces(textinfo="percent+label", textfont_size=11)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<div class='section-header' style='margin-top:20px;'>Promo Code Type Analysis</div>", unsafe_allow_html=True)

    promo_type = df[df["promo_code_type"].notna()].groupby("promo_code_type").agg(
        Revenue=("line_value_aed", "sum"),
        Quantity=("quantity", "sum"),
        Orders=("order_id", "count"),
        Avg_Discount=("discount_aed", "mean")
    ).reset_index().sort_values("Revenue", ascending=False)

    c4, c5 = st.columns(2)

    with c4:
        fig4 = px.bar(promo_type, x="promo_code_type", y="Revenue",
                      title="Revenue by Promo Type",
                      color="promo_code_type",
                      color_discrete_sequence=["#3b82f6", "#f59e0b", "#10b981", "#a78bfa"])
        fig4.update_layout(**TEMPLATE["layout"], height=300, showlegend=False)
        fig4.update_traces(marker_cornerradius=6)
        st.plotly_chart(fig4, use_container_width=True)

    with c5:
        fig5 = px.bar(promo_type, x="promo_code_type", y="Orders",
                      title="Transaction Count by Promo Type",
                      color="promo_code_type",
                      color_discrete_sequence=["#3b82f6", "#f59e0b", "#10b981", "#a78bfa"])
        fig5.update_layout(**TEMPLATE["layout"], height=300, showlegend=False)
        fig5.update_traces(marker_cornerradius=6)
        st.plotly_chart(fig5, use_container_width=True)

    # Promo type by city heatmap
    st.markdown("<div class='section-header' style='margin-top:20px;'>Promo Type Adoption by City</div>", unsafe_allow_html=True)
    pc = df[df["promo_code_type"].notna()].groupby(["city", "promo_code_type"])["order_id"].count().reset_index()
    pc_pivot = pc.pivot_table(index="city", columns="promo_code_type", values="order_id", fill_value=0)
    fig6 = go.Figure(go.Heatmap(
        z=pc_pivot.values, x=pc_pivot.columns, y=pc_pivot.index,
        colorscale=[[0, "#080c14"], [0.5, "#0c2d5a"], [1, "#06b6d4"]],
        showscale=True,
        colorbar=dict(thickness=8, tickfont=dict(color="#5a7499")),
        hovertemplate="City: %{y}<br>Type: %{x}<br>Count: %{z}<extra></extra>",
        text=pc_pivot.values,
        texttemplate="%{text}", textfont=dict(size=11, color="#7090b0"),
    ))
    fig6.update_layout(**TEMPLATE["layout"], height=300, title_text="Promo Type Usage Heatmap by City")
    st.plotly_chart(fig6, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 · PAYMENT INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-header'>Payment Method Distribution</div>", unsafe_allow_html=True)

    pay_df = df.groupby("payment_method").agg(
        Orders=("order_id", "count"),
        Revenue=("line_value_aed", "sum"),
        Avg_Value=("line_value_aed", "mean")
    ).reset_index().sort_values("Orders", ascending=False)

    c1, c2 = st.columns(2)

    with c1:
        fig = px.pie(pay_df, values="Orders", names="payment_method",
                     title="Transaction Share by Payment Method",
                     color_discrete_sequence=["#3b82f6", "#f59e0b", "#10b981", "#a78bfa", "#f43f5e"],
                     hole=0.5)
        fig.update_layout(**TEMPLATE["layout"], height=320)
        fig.update_traces(textinfo="percent+label", textfont_size=11,
                          marker=dict(line=dict(color="#080c14", width=2)))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.bar(pay_df.sort_values("Avg_Value"), x="Avg_Value", y="payment_method",
                      orientation="h",
                      title="Avg Order Value by Payment Method (AED)",
                      color="payment_method",
                      color_discrete_sequence=["#3b82f6", "#f59e0b", "#10b981", "#a78bfa", "#f43f5e"],
                      text="Avg_Value")
        fig2.update_traces(texttemplate="AED %{text:,.0f}", textposition="outside",
                           textfont=dict(color="#5a7499", size=10), marker_cornerradius=4)
        fig2.update_layout(**TEMPLATE["layout"], height=320, showlegend=False,
                           xaxis=dict(showticklabels=False, showgrid=False))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='section-header' style='margin-top:20px;'>Payment Preferences by City & Month</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)

    with c3:
        city_pay = df.groupby(["city", "payment_method"])["order_id"].count().reset_index()
        city_pay.columns = ["City", "Payment Method", "Orders"]
        fig3 = px.bar(city_pay, x="City", y="Orders", color="Payment Method",
                      title="Payment Method Mix by City",
                      color_discrete_sequence=["#3b82f6", "#f59e0b", "#10b981", "#a78bfa", "#f43f5e"],
                      barmode="stack")
        fig3.update_layout(**TEMPLATE["layout"], height=340)
        fig3.update_traces(marker_cornerradius=2)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        mon_pay = df.groupby(["order_month", "payment_method"])["order_id"].count().reset_index()
        mon_pay.columns = ["Month", "Payment Method", "Orders"]
        mon_pay["Month"] = mon_pay["Month"].str.replace("2025-", "", regex=False)
        fig4 = px.line(mon_pay, x="Month", y="Orders", color="Payment Method",
                       title="Payment Method Trend Over Time",
                       color_discrete_sequence=["#3b82f6", "#f59e0b", "#10b981", "#a78bfa", "#f43f5e"],
                       markers=True)
        fig4.update_layout(**TEMPLATE["layout"], height=340)
        fig4.update_traces(line_width=2, marker_size=7)
        st.plotly_chart(fig4, use_container_width=True)

    # Digital vs traditional
    st.markdown("<div class='section-header' style='margin-top:20px;'>Digital vs Traditional Payments</div>", unsafe_allow_html=True)
    df["payment_category"] = df["payment_method"].map({
        "Card": "Digital Card",
        "Wallet": "Digital Wallet",
        "Apple Pay": "Mobile Pay",
        "Google Pay": "Mobile Pay",
        "Cash": "Cash"
    })
    pay_cat = df.groupby(["order_month", "payment_category"])["order_id"].count().reset_index()
    pay_cat["Month"] = pay_cat["order_month"].str.replace("2025-", "", regex=False)
    fig5 = px.area(pay_cat, x="Month", y="order_id", color="payment_category",
                   title="Payment Category Adoption Trend",
                   color_discrete_sequence=["#3b82f6", "#10b981", "#f59e0b", "#f43f5e"],
                   labels={"order_id": "Orders"})
    fig5.update_layout(**TEMPLATE["layout"], height=280)
    st.plotly_chart(fig5, use_container_width=True)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='border-top: 1px solid #1a2540; margin-top: 32px; padding-top: 16px;
     text-align: center; font-size: 11px; color: #2a3d56;'>
  LuLu UAE Retail Intelligence Dashboard · Built with Streamlit & Plotly · Data: Apr–Oct 2025
</div>
""", unsafe_allow_html=True)
