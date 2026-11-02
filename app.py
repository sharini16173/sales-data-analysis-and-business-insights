# 1. Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 2. Configure the dashboard (Wide layout)
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Superstore Sales Analysis Dashboard")
st.write("Explore sales and profit performance by year.")

# 3. Load the dataset
df = pd.read_csv("outputs/cleaned_sales.csv", encoding="latin1")

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

# 4. Create sidebar filter (Year Slicer only)
st.sidebar.header("Dashboard Filters")

year_options = ["All Years", 2014, 2015, 2016, 2017]
selected_year = st.sidebar.selectbox(
    "Select Year",
    year_options,
    index=0
)

# Apply Year Filter
if selected_year == "All Years":
    year_df = df.copy()
    display_title = "Overall Performance - All Years (2014-2017)"
else:
    year_df = df[df["Order Date"].dt.year == selected_year].copy()
    display_title = f"Overall Performance - {selected_year}"

if year_df.empty:
    st.warning("No records found for the selected year.")
    st.stop()

# 5. Calculate the overall KPIs for the selected view
total_sales = year_df["Sales"].sum()
total_profit = year_df["Profit"].sum()
total_orders = year_df["Order ID"].nunique()
total_customers = year_df["Customer ID"].nunique()

# 6. Calculate monthly sales, profit, orders and customers
year_df["Month_Number"] = year_df["Order Date"].dt.month

monthly_data = year_df.groupby("Month_Number").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique"),
    Customers=("Customer ID", "nunique")
).reindex(range(1, 13), fill_value=0)

# 7. Calculate latest month vs previous month (only applicable for single years)
if selected_year != "All Years":
    months_with_data = sorted(year_df["Order Date"].dt.month.unique())
    latest_month = months_with_data[-1] if months_with_data else 1
    previous_month = latest_month - 1 if latest_month > 1 else None

    def calculate_change(current, previous):
        if previous == 0:
            return None
        return ((current - previous) / abs(previous)) * 100

    if previous_month is not None:
        sales_change = calculate_change(monthly_data.loc[latest_month, "Sales"], monthly_data.loc[previous_month, "Sales"])
        profit_change = calculate_change(monthly_data.loc[latest_month, "Profit"], monthly_data.loc[previous_month, "Profit"])
        orders_change = calculate_change(monthly_data.loc[latest_month, "Orders"], monthly_data.loc[previous_month, "Orders"])
        customers_change = calculate_change(monthly_data.loc[latest_month, "Customers"], monthly_data.loc[previous_month, "Customers"])
    else:
        sales_change = profit_change = orders_change = customers_change = None

    caption_text = f"Monthly comparison: {pd.Timestamp(selected_year, latest_month, 1):%B %Y}" + (f" vs {pd.Timestamp(selected_year, previous_month, 1):%B %Y}" if previous_month is not None else " (no earlier month available)")
else:
    sales_change = profit_change = orders_change = customers_change = None
    caption_text = "Aggregated performance overview across all years (2014-2017)"

def change_text(change):
    if change is None:
        return "N/A"
    if change > 0:
        return f"📈 {change:.2f}% increase"
    if change < 0:
        return f"📉 {abs(change):.2f}% decrease"
    return "No change"

# 8. Display KPI cards in ultra-compact boxes with headings above
st.subheader(display_title)
st.caption(caption_text)

col1, col2, col3, col4 = st.columns(4)

# KPI 1: Sales
with col1:
    st.markdown(
        """
        <div style="background-color:#F5F8FC; padding:8px; border-radius:6px;">
            <p style="color:#555; margin:0; font-size:12px;">Total Sales</p>
        """,
        unsafe_allow_html=True
    )
    st.metric("Sales", f"${total_sales:,.2f}", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    if selected_year != "All Years":
        st.caption(change_text(sales_change))
    else:
        st.caption("All-time aggregate (2014-2017)")

# KPI 2: Profit
with col2:
    st.markdown(
        """
        <div style="background-color:#F5F8FC; padding:8px; border-radius:6px;">
            <p style="color:#555; margin:0; font-size:12px;">Total Profit</p>
        """,
        unsafe_allow_html=True
    )
    st.metric("Profit", f"${total_profit:,.2f}", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    if selected_year != "All Years":
        st.caption(change_text(profit_change))
    else:
        st.caption("All-time aggregate (2014-2017)")

# KPI 3: Orders
with col3:
    st.markdown(
        """
        <div style="background-color:#F5F8FC; padding:8px; border-radius:6px;">
            <p style="color:#555; margin:0; font-size:12px;">Total Orders</p>
        """,
        unsafe_allow_html=True
    )
    st.metric("Orders", f"{total_orders:,}", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    if selected_year != "All Years":
        st.caption(change_text(orders_change))
    else:
        st.caption("All-time aggregate (2014-2017)")

# KPI 4: Customers
with col4:
    st.markdown(
        """
        <div style="background-color:#F5F8FC; padding:8px; border-radius:6px;">
            <p style="color:#555; margin:0; font-size:12px;">Total Customers</p>
        """,
        unsafe_allow_html=True
    )
    st.metric("Customers", f"{total_customers:,}", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    if selected_year != "All Years":
        st.caption(change_text(customers_change))
    else:
        st.caption("All-time aggregate (2014-2017)")

st.markdown("<br>", unsafe_allow_html=True)

# 9. Monthly Sales History - Ultra-Compact Line Chart
st.subheader("1. Monthly Sales History")

month_names = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
]

monthly_sales = monthly_data["Sales"]

fig, ax = plt.subplots(figsize=(8, 2.4))
ax.plot(
    month_names,
    monthly_sales.values,
    marker="o",
    color="#1f77b4",
    linewidth=1.5,
    markersize=4
)

ax.set_title("Monthly Sales Trend", fontsize=9)
ax.set_ylabel("Sales ($)", fontsize=7)

ax.set_xticks(range(12))
ax.set_xticklabels(month_names, fontsize=7)
ax.tick_params(axis='y', labelsize=7)

ax.grid(axis="y", linestyle="--", alpha=0.3)
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

# 10, 11, 12. Category and Region Charts arranged in side-by-side columns
col_a, col_b = st.columns(2)

with col_a:
    # Sales by Category
    st.subheader("2. Sales by Category")
    category_sales = year_df.groupby("Category")["Sales"].sum()

    fig, ax = plt.subplots(figsize=(5, 2.4))
    bars = ax.bar(category_sales.index, category_sales.values, color="#1f77b4", width=0.5)

    ax.set_ylim(0, category_sales.max() * 1.20)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"${height:,.0f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha='center', va='bottom', fontsize=7
        )

    ax.set_title("Sales by Category", fontsize=9)
    ax.set_ylabel("Sales ($)", fontsize=7)
    ax.tick_params(axis="x", rotation=0, labelsize=7)
    ax.tick_params(axis='y', labelsize=7)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # Sales by Region
    st.subheader("4. Sales by Region")
    region_sales = year_df.groupby("Region")["Sales"].sum()

    fig, ax = plt.subplots(figsize=(5, 2.4))
    bars = ax.bar(region_sales.index, region_sales.values, color="#1f77b4", width=0.5)

    ax.set_ylim(0, region_sales.max() * 1.20)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"${height:,.0f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha='center', va='bottom', fontsize=7
        )

    ax.set_title("Sales by Region", fontsize=9)
    ax.set_ylabel("Sales ($)", fontsize=7)
    ax.tick_params(axis="x", rotation=15, labelsize=7)
    ax.tick_params(axis='y', labelsize=7)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col_b:
    # Profit by Category
    st.subheader("3. Profit by Category")
    category_profit = year_df.groupby("Category")["Profit"].sum()

    max_p = category_profit.max()
    min_p = min(0, category_profit.min())
    
    fig, ax = plt.subplots(figsize=(5, 2.4))
    bars = ax.bar(category_profit.index, category_profit.values, color="#1f77b4", width=0.5)

    ax.set_ylim(min_p * 1.1, max_p * 1.25)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"${height:,.0f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3 if height >= 0 else -10),
            textcoords="offset points",
            ha='center', va='bottom' if height >= 0 else 'top', fontsize=7
        )

    ax.set_title("Profit by Category", fontsize=9)
    ax.set_ylabel("Profit ($)", fontsize=7)
    ax.tick_params(axis="x", rotation=0, labelsize=7)
    ax.tick_params(axis='y', labelsize=7)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# 13. Footer
st.divider()
st.caption("Built with Python, Pandas, Matplotlib, and Streamlit.")
