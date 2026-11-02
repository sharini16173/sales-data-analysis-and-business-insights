# 1. Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# 2. Configure the dashboard
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Superstore Sales Analysis Dashboard")
st.write("Explore sales and profit performance by year.")


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
# Find the last month that has actual records
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


# 8. Display KPI cards in light-coloured boxes
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
                    padding:18px;border-radius:10px;">
            <p style="color:#555;margin:0;">Total Sales</p>
        """,
        unsafe_allow_html=True
    )
    st.metric("Sales", f"${total_sales:,.2f}", label_visibility="collapsed")
    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )
    st.caption(change_text(sales_change))


# KPI 2: Profit
with col2:
    st.markdown(
        """
        <div style="background-color:#F5F8FC;
                    padding:18px;border-radius:10px;">
            <p style="color:#555;margin:0;">Total Profit</p>
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
                    padding:18px;border-radius:10px;">
            <p style="color:#555;margin:0;">Total Orders</p>
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
                    padding:18px;border-radius:10px;">
            <p style="color:#555;margin:0;">Total Customers</p>
        """,
        unsafe_allow_html=True
    )
    st.metric("Customers", f"{total_customers:,}", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption(change_text(customers_change))


st.divider()


# 9. Monthly Sales History - Matplotlib
st.subheader("1. Monthly Sales History")

month_names = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

monthly_sales = monthly_data["Sales"]

fig, ax = plt.subplots(figsize=(12, 4))

ax.plot(
    month_names,
    monthly_sales.values,
    marker="o"
)

ax.set_title(f"Monthly Sales Trend - {selected_year}")
ax.set_xlabel("Month")
ax.set_ylabel("Sales ($)")

# Show all month names clearly
ax.set_xticks(range(12))
ax.set_xticklabels(month_names, rotation=35, ha="right")

ax.grid(axis="y", linestyle="--", alpha=0.3)
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)


st.divider()


# 10. Sales by Category - Matplotlib
st.subheader("2. Sales by Category")

category_sales = year_df.groupby("Category")["Sales"].sum()

fig, ax = plt.subplots(figsize=(8, 4))

category_sales.plot(kind="bar", ax=ax)

ax.set_title(f"Sales by Category - {selected_year}")
ax.set_xlabel("Category")
ax.set_ylabel("Sales ($)")
ax.tick_params(axis="x", rotation=0)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)


st.divider()


# 11. Profit by Category - Matplotlib
st.subheader("3. Profit by Category")

category_profit = year_df.groupby("Category")["Profit"].sum()

fig, ax = plt.subplots(figsize=(8, 4))

category_profit.plot(kind="bar", ax=ax)

ax.set_title(f"Profit by Category - {selected_year}")
ax.set_xlabel("Category")
ax.set_ylabel("Profit ($)")
ax.tick_params(axis="x", rotation=0)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)


st.divider()


# 12. Sales by Region - Plotly Express
st.subheader("4. Sales by Region")

region_sales = year_df.groupby(
    "Region", as_index=False
)["Sales"].sum()

fig = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title=f"Sales by Region - {selected_year}"
)

fig.update_layout(
    height=350,
    xaxis_title="Region",
    yaxis_title="Sales ($)"
)

st.plotly_chart(fig, use_container_width=True)


# 13. Footer
st.divider()

st.caption(
    "Built with Python, Pandas, Matplotlib, "
    "Plotly Express and Streamlit."
)
