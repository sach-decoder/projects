
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path 

csv_path = Path(__file__).parent / "transformed_company_data.csv"
df = pd.read_csv(csv_path)
df = df.drop(columns=['Company Path'])

st.set_page_config(page_title="Company Dashboard", layout="wide")
st.title("Company Analytics Dashboard")

def kpi_card():
    st.subheader("Company Revenues")
    df_revenue_kpi = df.set_index('Company')['revenue'].to_dict()
    companies = list(df_revenue_kpi.keys())
    
    num_cols = 3
    cols = st.columns(num_cols)
    
    for i in range(min(15, len(companies))):
        company = companies[i]
        revenue = df_revenue_kpi[company]
        
        cols[i % num_cols].metric(
            label=f"{company} Total Revenue", 
            value=f"${revenue:,}", 
            delta="+12%", 
            border=True
        )

def scatter_plot():
    st.subheader("Revenue Heatmap (Plotly)")

    df['debt_ratio'] = df['total-debt'] / df['total-assets'] * 100

    fig = px.density_heatmap(
        df, 
        x="Country", 
        y="Industry", 
        z="debt_ratio", 
        histfunc="sum",          
        color_continuous_scale="Viridis",
        text_auto=True            
    )

    st.plotly_chart(fig, use_container_width=True)

def tree_map():
    st.subheader("Industry Size by Revenue")
    fig = px.treemap(df, path=["Industry"], values="revenue")
    st.plotly_chart(fig, use_container_width=True)

def bubble_chart():
    st.subheader("# of Employees vs Market cap")

    for col in ["revenue", "employees", "marketcap"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    plot_df = df.dropna(subset=["employees", "marketcap"]).copy()

    plot_df["revenue"] = plot_df["revenue"].fillna(0)

    plot_df.loc[plot_df["revenue"] < 0, "revenue"] = 0

    fig = px.scatter(
        plot_df,
        x="employees",
        y="marketcap",
        size="revenue",
        color="Company",
        size_max=60,
        title="My Bubble Chart",
    )

    st.plotly_chart(fig, use_container_width=True)

def bar_chart():
    st.subheader('total-assests vs total-liabilities')
    df['company_equity'] = df['total-assets'] - df['total-liabilities']
    fig = px.bar(df, x='Company', y='company_equity')
    st.plotly_chart(fig)

kpi_card()

st.divider()

col1, col2 = st.columns(2)

with col1:
    scatter_plot()

with col2:
    tree_map()

st.divider()

col3, col4 = st.columns(2)

with col3:
    bubble_chart()

with col4:
    bar_chart()
