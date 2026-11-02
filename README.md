# 🛒 Superstore Sales & Profitability Analysis

> **An entry-level data analytics portfolio project that uncovers retail sales trends, financial profit leaks, and business strategies using Python and SQLite.**

---

## 📋 Executive Summary / Overview
This project analyzes four years of sales data from a retail store to identify what drives profit and what causes losses. The analysis reveals that offering high discounts (30% or more) leads to financial losses instead of helping the business. The findings provide clear, data-driven advice on how to fix pricing strategies and grow profits, combining business administration principles with data analytics.

---

## 📂 Dataset Description
* **Dataset Name:** Sample Superstore Dataset[cite: 1]
* **Total Rows & Columns:** 9,994 rows and 21 columns[cite: 1]
* **Key Columns Used:**
  * `Order Date` & `Ship Date`: The dates when items were ordered and shipped[cite: 1].
  * `Customer Name` & `Segment`: Who bought the items (Consumer, Corporate, or Home Office)[cite: 1].
  * `Category` & `Sub-Category`: The type of product (such as Furniture, Office Supplies, or Technology)[cite: 1].
  * `Sales` & `Profit`: How much money the item sold for and how much profit (or loss) it made[cite: 1].
  * `Discount`: The percentage discount given on the sale[cite: 1].

---

## 🛠️ Tools & Libraries Used
* **Programming Language:** Python
* **Data Analysis Library:** Pandas (used for cleaning and sorting data)
* **Database Tools:** DB Browser for SQLite (for managing and querying local dataset files)
* **Data Visualization Libraries:** Matplotlib and Seaborn (used for drawing charts and graphs)
* **Environment:** Jupyter Notebook
* **Version Control & Hosting:** Git and GitHub

---

## 🧹 Data Cleaning & Preparation
Before looking at the numbers, the data was cleaned and prepared:
* **Checking for Missing Values:** Checked the entire dataset and confirmed there were no missing or blank cells[cite: 1].
* **Fixing Data Types:** Changed the order and shipping dates from plain text into real date formats so we could easily sort by year and month[cite: 1].
* **Creating New Columns:** Added new columns like `Year`, `Month`, `Shipping Days`, and a `Profit Status` tag (labeling each order as either a "Profit" or a "Loss") to make sorting easier[cite: 1].

---

## 📈 Exploratory Data Analysis (EDA) & Key Insights

1. **The Discount Trap:**
   * Looking at the discount levels, any discount set at **30% or higher** always results in a net financial loss[cite: 1]. Giving away deep discounts hurts the business instead of helping it.
2. **Category Performance:**
   * **Technology** and **Office Supplies** are very profitable, bringing in steady profit margins of around 17%[cite: 1]. 
   * On the other hand, **Furniture** brings in high sales volume but a very low profit margin of only 2.49%[cite: 1].
3. **Loss-Making Sub-Categories:**
   * **Tables** and **Bookcases** are the biggest money-losers in the store, mostly because heavy items are sold with high discounts that wipe out all the profit[cite: 1].
4. **Sales Seasonality:**
   * Customer orders grow steadily throughout the year and spike heavily during the last few months, peaking in September, November, and December[cite: 1].

---

## 💻 Code Snippets & Analysis Highlights

Here is a simple example of how the data was grouped by category to check total sales and profits using Python:

```python
# Grouping data by product category to see total sales and profit
category_analysis = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Total_Profit=("Profit", "sum")
)
print(category_analysis.sort_values("Total_Sales", ascending=False))
```

Here is how we filtered the data to count how many orders resulted in a financial loss:

```python
# Finding orders with a negative total profit (losses)
order_analysis = df.groupby("Order ID").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
)
loss_orders = order_analysis[order_analysis["Total_Profit"] < 0]
print("Number of loss-making orders:", len(loss_orders))
```

---

## 💡 Recommendations & Business Impact

* **Limit Discounts:** Set a strict maximum discount limit of **20%** to stop losing money on heavy discounts.
* **Fix Furniture Pricing:** Review shipping and pricing rules for **Tables** and **Bookcases** so they stop losing money for the store.
* **Prepare for Busy Seasons:** Make sure inventory and marketing campaigns are fully ready ahead of the busy holiday shopping months (September through December).

---

## 🚀 How to Run the Project

1. Clone this repository to your computer:
   ```bash
   git clone [https://github.com/your-username/superstore-sales-analysis.git](https://github.com/your-username/superstore-sales-analysis.git)
   ```
2. Install the required Python libraries:
   ```bash
   pip install pandas matplotlib seaborn openpyxl
   ```
3. Open the Jupyter Notebook to view all code, charts, and findings:
   ```bash
   jupyter notebook Superstore_Sales.ipynb
   ```
