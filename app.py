import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")

# Load dataset safely
@st.cache_data
def load_data():
    return pd.read_csv("outputs/cleaned_superstore.csv", encoding="latin1")

df = load_data()

# Sidebar year filter
st.sidebar.header("Dashboard Filters")
selected_year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique()))
filtered_df = df[df['Year'] == selected_year]

# Main Dashboard Title
st.title(f"Overall Performance - {selected_year}")

# Top KPI Metric Cards
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['Order_ID'].count()
total_customers = filtered_df['Customer_ID'].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Total Customers", f"{total_customers:,}")

st.markdown("---")

# 1. Monthly Sales Trend (Line Chart using Matplotlib)
st.subheader("1. Monthly Sales History")
monthly_sales = filtered_df.groupby('Month_Name')['Sales'].sum()

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(monthly_sales.index, monthly_sales.values, marker='o', color="#1f77b4", linewidth=2)
ax1.set_title(f"Monthly Sales Trend - {selected_year}")
ax1.set_ylabel("Sales ($)")
plt.xticks(rotation=45)
st.pyplot(fig1)

# 2. First Bar Chart (Sales by Category using Matplotlib)
st.subheader("2. Sales by Category")
category_sales = filtered_df.groupby('Category')['Sales'].sum()

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.bar(category_sales.index, category_sales.values, color="#1f77b4")
ax2.set_title(f"Sales Distribution by Category - {selected_year}")
ax2.set_ylabel("Sales ($)")
st.pyplot(fig2)

# 3. Third Chart (Bar Chart using Matplotlib - Plotly Removed)
st.subheader("3. Sales Breakdown")
group_col = 'Sub-Category' if 'Sub-Category' in df.columns else 'Region'
bar_data = filtered_df.groupby(group_col)['Sales'].sum()

fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.bar(bar_data.index, bar_data.values, color="#1f77b4")
ax3.set_title(f"Sales Breakdown by {group_col} - {selected_year}")
ax3.set_ylabel("Sales ($)")
plt.xticks(rotation=45)
st.pyplot(fig3)
