# 1. Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px


# 2. Configure the dashboard
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS to reduce text sizes, make everything compact, and improve the fresher look
st.markdown("""
    <style>
        h1 {font-size: 24px !important; color: #1f77b4; margin-bottom: 0px;}
        h2, .stSubheader {font-size: 16px !important; font-weight: 600; margin-top: 10px; margin-bottom: 5px;}
        p, .stCaption {font-size: 12px !important;}
        .block-container {padding-top: 1.5rem; padding-bottom: 1rem;}
    </style>
""", unsafe_allow_html=True)

st.title("Superstore Sales Analysis Dashboard")
st.write("Explore sales and profit performance across years.")


# 3. Load the dataset
df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

# Clean column names
df.columns = df.columns.str.strip()

# Convert Order Date into datetime format
df["Order Date"] = pd.to_datetime(
    df["Order Date"], errors="coerce"
)

# Remove rows with missing or invalid order dates
df = df.dropna(subset=["Order Date"])

# Keep only the requested years
df = df[
    (df["Order Date"].dt.year >= 2014) &
    (df["Order Date"].dt.year <= 2017)
].copy()

if df.empty:
    st.error("No data found between 2014 and 2017.")
    st.stop()


# 4. Create the year slicer with an "All" option
st.sidebar.header("Dashboard Filters")

year_options = ["All"] + [2014, 2015, 2016, 2017]
selected_year = st.sidebar.selectbox(
    "Select Year",
    year_options,
    index=0  # Defaults to "All"
)

# Filter data based on selection ("All" or specific year)
if selected_year == "All":
    year_df = df.copy()
    filter_label = "All Years (2014 - 2017)"
else:
    year_df = df[df["Order Date"].dt.year == selected_year].copy()
    filter_label = f"Year: {selected_year}"

if year_df.empty:
    st.warning(f"No records found for {selected_year}.")
    st.stop()


# 5. Calculate the overall KPIs for the selected view
total_sales = year_df["Sales"].sum()
total_profit = year_df["Profit"].sum()
total_orders = year_df["Order ID"].nunique()
total_customers = year_df["Customer ID"].nunique()


# 6. Calculate monthly metrics for trend comparison
year_df["Month_Year"] = year_df["Order Date"].dt.to_period("M")

if selected_year == "All":
    trend_data = year_df.groupby("Month_Year").agg(
        Sales=("Sales", "sum")
    ).reset_index()
    trend_data["Month_Year"] = trend_data["Month_Year"].astype(str)
else:
    year_df["Month_Number"] = year_df["Order Date"].dt.month
    monthly_data = year_df.groupby("Month_Number").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique"),
        Customers=("Customer ID", "nunique")
    ).reindex(range(1, 13), fill_value=0)
    
    months_with_data = sorted(year_df["Order Date"].dt.month.unique())
    latest_month = months_with_data[-1] if months_with_data else 1
    previous_month = latest_month - 1 if latest_month > 1 else None


# 7. Helper functions for formatting changes
def calculate_change(current, previous):
    if previous == 0 or previous is None:
        return None
    return ((current - previous) / abs(previous)) * 100

def change_text(change):
    if change is None:
        return ""
    if change > 0:
        return f"📈 +{change:.1f}% vs prev"
    if change < 0:
        return f"📉 -{abs(change):.1f}% vs prev"
    return "No change"


# 8. Display KPI cards in compact layout
st.subheader(f"Overall Performance — {filter_label}")

if selected_year != "All" and previous_month is not None:
    st.caption(f"Monthly comparison: {pd.Timestamp(selected_year, latest_month, 1):%B %Y} vs {pd.Timestamp(selected_year, previous_month, 1):%B %Y}")
else:
    st.caption("Cumulative metrics based on current filter selection.")

col1, col2, col3, col4 = st.columns(4)

if selected_year != "All" and previous_month is not None:
    sales_change = calculate_change(monthly_data.loc[latest_month, "Sales"], monthly_data.loc[previous_month, "Sales"])
    profit_change = calculate_change(monthly_data.loc[latest_month, "Profit"], monthly_data.loc[previous_month, "Profit"])
    orders_change = calculate_change(monthly_data.loc[latest_month, "Orders"], monthly_data.loc[previous_month, "Orders"])
    customers_change = calculate_change(monthly_data.loc[latest_month, "Customers"], monthly_data.loc[previous_month, "Customers"])
else:
    sales_change = profit_change = orders_change = customers_change = None

def render_kpi_card(title, value, change_val):
    subtext = change_text(change_val) if (selected_year != "All" and change_val is not None) else ""
    st.markdown(
        f"""
        <div style="background-color:#F8FAFC; padding:8px 12px; border-radius:6px; border: 1px solid #E2E8F0;">
            <p style="color:#64748B; font-size:11px !important; margin:0 0 2px 0; font-weight:500;">{title}</p>
            <h3 style="color:#0F172A; font-size:18px !important; margin:0 0 2px 0;">{value}</h3>
            <p style="font-size:10px !important; color:#475569; margin:0;">{subtext}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col1:
    render_kpi_card("Total Sales", f"${total_sales:,.2f}", sales_change)
with col2:
    render_kpi_card("Total Profit", f"${total_profit:,.2f}", profit_change)
with col3:
    render_kpi_card("Total Orders", f"{total_orders:,}", orders_change)
with col4:
    render_kpi_card("Total Customers", f"{total_customers:,}", customers_change)


st.divider()


# 9. Sales Trend Analysis (Line Chart)
st.subheader("1. Sales Trend Analysis")

if selected_year == "All":
    fig_trend = px.line(trend_data, x="Month_Year", y="Sales", markers=True)
else:
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_sales_df = pd.DataFrame({"Month": month_names, "Sales": monthly_data["Sales"].values})
    fig_trend = px.line(monthly_sales_df, x="Month", y="Sales", markers=True)

fig_trend.update_traces(line_color="#2563EB")
fig_trend.update_layout(
    height=260,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis_title="",
    yaxis_title="Sales ($)",
    font=dict(size=10)
)
st.plotly_chart(fig_trend, use_container_width=True)


st.divider()


# 10 & 11. Side-by-Side Layout for Category Sales & Profit Charts (Interactive Hover with uniform blue color)
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("2. Sales by Category")
    category_sales = year_df.groupby("Category", as_index=False)["Sales"].sum()

    fig_cat_sales = px.bar(
        category_sales,
        x="Category",
        y="Sales"
    )
    fig_cat_sales.update_traces(marker_color="#2563EB")
    fig_cat_sales.update_layout(
        height=240,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="",
        yaxis_title="Sales ($)",
        font=dict(size=10)
    )
    st.plotly_chart(fig_cat_sales, use_container_width=True)

with col_chart2:
    st.subheader("3. Profit by Category")
    category_profit = year_df.groupby("Category", as_index=False)["Profit"].sum()

    fig_cat_profit = px.bar(
        category_profit,
        x="Category",
        y="Profit"
    )
    fig_cat_profit.update_traces(marker_color="#2563EB")
    fig_cat_profit.update_layout(
        height=240,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="",
        yaxis_title="Profit ($)",
        font=dict(size=10)
    )
    st.plotly_chart(fig_cat_profit, use_container_width=True)


st.divider()


# 12. Sales by Region - Plotly Bar Chart (No permanent labels, uniform blue color, hover to see values)
st.subheader("4. Sales by Region")

region_sales = year_df.groupby(
    "Region", as_index=False
)["Sales"].sum()

fig_region = px.bar(
    region_sales,
    x="Region",
    y="Sales"
)

fig_region.update_traces(marker_color="#2563EB")
fig_region.update_layout(
    height=240,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis_title="",
    yaxis_title="Sales ($)",
    font=dict(size=10)
)

st.plotly_chart(fig_region, use_container_width=True)


# 13. Footer
st.divider()
st.caption("Superstore Analytics Portfolio Project | Built with Python, Pandas, Plotly, and Streamlit.")
