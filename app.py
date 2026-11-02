# 1. Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# 2. Configure the dashboard
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


# 4. Create the year slicer
st.sidebar.header("Dashboard Filters")

selected_year = st.sidebar.selectbox(
    "Select Year",
    [2014, 2015, 2016, 2017],
    index=3
)

# Filter data for the selected year
year_df = df[
    df["Order Date"].dt.year == selected_year
].copy()

if year_df.empty:
    st.warning(f"No records found for {selected_year}.")
    st.stop()


# 5. Calculate the overall KPIs for the selected year
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
)

# Include all 12 months, even if a month has no records
monthly_data = monthly_data.reindex(
    range(1, 13), fill_value=0
)


# 7. Calculate the latest available month vs previous month
months_with_data = sorted(
    year_df["Order Date"].dt.month.unique()
)

latest_month = months_with_data[-1]

if latest_month > 1:
    previous_month = latest_month - 1
else:
    previous_month = None


def calculate_change(current, previous):
    if previous == 0:
        return None
    return ((current - previous) / abs(previous)) * 100


def change_text(change):
    if change is None:
        return "N/A - previous month has zero value"
    if change > 0:
        return f"📈 {change:.2f}% increase"
    if change < 0:
        return f"📉 {abs(change):.2f}% decrease"
    return "No change"


# 8. Display KPI cards in light-coloured compact boxes
st.subheader(f"Overall Performance - {selected_year}")

st.caption(
    f"Monthly comparison: "
    f"{pd.Timestamp(selected_year, latest_month, 1):%B %Y}"
    + (
        f" vs {pd.Timestamp(selected_year, previous_month, 1):%B %Y}"
        if previous_month is not None
        else " (no earlier month available)"
    )
)

col1, col2, col3, col4 = st.columns(4)

# Calculate monthly changes
if previous_month is not None:
    sales_change = calculate_change(
        monthly_data.loc[latest_month, "Sales"],
        monthly_data.loc[previous_month, "Sales"]
    )
    profit_change = calculate_change(
        monthly_data.loc[latest_month, "Profit"],
        monthly_data.loc[previous_month, "Profit"]
    )
    orders_change = calculate_change(
        monthly_data.loc[latest_month, "Orders"],
        monthly_data.loc[previous_month, "Orders"]
    )
    customers_change = calculate_change(
        monthly_data.loc[latest_month, "Customers"],
        monthly_data.loc[previous_month, "Customers"]
    )
else:
    sales_change = None
    profit_change = None
    orders_change = None
    customers_change = None


# KPI 1: Sales
with col1:
    st.markdown(
        """
        <div style="background-color:#F5F8FC;
                    padding:10px;border-radius:8px;">
            <p style="color:#555;margin:0;font-size:14px;">Total Sales</p>
        """,
        unsafe_allow_html=True
    )
    st.metric("Sales", f"${total_sales:,.2f}", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption(change_text(sales_change))


# KPI 2: Profit
with col2:
    st.markdown(
        """
        <div style="background-color:#F5F8FC;
                    padding:10px;border-radius:8px;">
            <p style="color:#555;margin:0;font-size:14px;">Total Profit</p>
        """,
        unsafe_allow_html=True
    )
    st.metric("Profit", f"${total_profit:,.2f}", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption(change_text(profit_change))


# KPI 3: Orders
with col3:
    st.markdown(
        """
        <div style="background-color:#F5F8FC;
                    padding:10px;border-radius:8px;">
            <p style="color:#555;margin:0;font-size:14px;">Total Orders</p>
        """,
        unsafe_allow_html=True
    )
    st.metric("Orders", f"{total_orders:,}", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption(change_text(orders_change))


# KPI 4: Customers
with col4:
    st.markdown(
        """
        <div style="background-color:#F5F8FC;
                    padding:10px;border-radius:8px;">
            <p style="color:#555;margin:0;font-size:14px;">Total Customers</p>
        """,
        unsafe_allow_html=True
    )
    st.metric("Customers", f"{total_customers:,}", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption(change_text(customers_change))

st.markdown("<br>", unsafe_allow_html=True)


# 9. Monthly Sales History - Compact Line Chart
st.subheader("1. Monthly Sales History")

month_names = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

monthly_sales = monthly_data["Sales"]

fig, ax = plt.subplots(figsize=(10, 3.2))

ax.plot(
    month_names,
    monthly_sales.values,
    marker="o",
    color="#1f77b4",
    linewidth=1.8
)

ax.set_title(f"Monthly Sales Trend - {selected_year}", fontsize=11)
ax.set_ylabel("Sales ($)", fontsize=9)

ax.set_xticks(range(12))
ax.set_xticklabels(month_names, rotation=30, ha="right", fontsize=8)
ax.tick_params(axis='y', labelsize=8)

ax.grid(axis="y", linestyle="--", alpha=0.3)
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)


# 10. Sales by Category - Compact Bar Chart
st.subheader("2. Sales by Category")

category_sales = year_df.groupby("Category")["Sales"].sum()

fig, ax = plt.subplots(figsize=(7, 3.2))

bars = ax.bar(category_sales.index, category_sales.values, color="#1f77b4", width=0.55)

for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f"${height:,.0f}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 2),
        textcoords="offset points",
        ha='center', va='bottom', fontsize=8
    )

ax.set_title(f"Sales by Category - {selected_year}", fontsize=11)
ax.set_ylabel("Sales ($)", fontsize=9)
ax.tick_params(axis="x", rotation=0, labelsize=8)
ax.tick_params(axis='y', labelsize=8)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)


# 11. Profit by Category - Compact Bar Chart
st.subheader("3. Profit by Category")

category_profit = year_df.groupby("Category")["Profit"].sum()

fig, ax = plt.subplots(figsize=(7, 3.2))

bars = ax.bar(category_profit.index, category_profit.values, color="#1f77b4", width=0.55)

for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f"${height:,.0f}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 2),
        textcoords="offset points",
        ha='center', va='bottom', fontsize=8
    )

ax.set_title(f"Profit by Category - {selected_year}", fontsize=11)
ax.set_ylabel("Profit ($)", fontsize=9)
ax.tick_params(axis="x", rotation=0, labelsize=8)
ax.tick_params(axis='y', labelsize=8)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)


# 12. Sales by Region - Compact Bar Chart
st.subheader("4. Sales by Region")

region_sales = year_df.groupby("Region")["Sales"].sum()

fig, ax = plt.subplots(figsize=(7, 3.2))

bars = ax.bar(region_sales.index, region_sales.values, color="#1f77b4", width=0.55)

for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f"${height:,.0f}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 2),
        textcoords="offset points",
        ha='center', va='bottom', fontsize=8
    )

ax.set_title(f"Sales by Region - {selected_year}", fontsize=11)
ax.set_ylabel("Sales ($)", fontsize=9)
ax.tick_params(axis="x", rotation=0, labelsize=8)
ax.tick_params(axis='y', labelsize=8)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)


# 13. Footer
st.divider()

st.caption(
    "Built with Python, Pandas, Matplotlib, "
    "and Streamlit."
)
