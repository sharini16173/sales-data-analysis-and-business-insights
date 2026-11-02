# 📊 Sales Data Analysis & Business Insights System

## 1. Project Objectives

The objective of this project is to analyze retail sales data to understand business performance, identify profitability challenges, and discover opportunities for improvement.

- Analyze overall sales, profit, orders, and customer performance.
- Identify high-performing and low-performing product categories.
- Evaluate regional sales and profitability.
- Understand monthly sales trends and month-on-month growth.
- Analyze customer purchasing patterns.
- Investigate the relationship between discounts and profitability.
- Identify loss-making orders and product sub-categories.
- Generate actionable business recommendations based on data-driven insights.

## 2. Skills and Technologies Showcased

**Programming & Data Analysis**
- Python
- Pandas
- NumPy

**Data Visualization**
- Matplotlib
- Seaborn

**Tools & Environment**
- Jupyter Notebook
- Excel
- Streamlit

**Analytical Skills**
- Data Cleaning and Preprocessing
- Exploratory Data Analysis (EDA)
- Feature Engineering
- Business KPI Analysis
- Data Aggregation and Grouping
- Time-Series Analysis
- Customer and Product Analysis
- Profitability Analysis
- Data Visualization
- Business Insights and Recommendations

## 3. Repository Structure

```text
Sales-Data-Analysis-and-Business-Insights/
│
├── outputs/
│   ├── cleaned_sales.csv
│   ├── sales_analysis.xlsx
│   ├── monthly_sales.png
│   ├── category_sales.png
│   ├── subcategory_profit.png
│   ├── region_sales.png
│   ├── sales_distribution.png
│   └── discount_profit.png
│
├── README.md
├── Sample - Superstore.csv
├── Superstore_Sales.ipynb
├── app.py
└── requirements.txt
```

**File Descriptions:**

- `outputs/` – Stores cleaned data, analysis reports, and generated visualizations.
- `README.md` – Project documentation.
- `Sample - Superstore.csv` – Original retail sales dataset.
- `Superstore_Sales.ipynb` – Jupyter Notebook containing the complete Python analysis.
- `app.py` – Python application for the sales analysis project.
- `requirements.txt` – Required Python libraries and dependencies.

## 4. Analytical Workflow

### Step 1: Data Loading & Understanding
- Imported the dataset using Pandas.
- Examined dataset dimensions, column names, and data types.
- Checked missing values and duplicate records.
- Analyzed descriptive statistics.

### Step 2: Data Cleaning & Preprocessing
- Standardized column names.
- Converted Order Date and Ship Date into datetime format.
- Inspected invalid sales and quantity values.
- Examined negative profit transactions.

### Step 3: Feature Engineering

Created additional columns to support business analysis:

- Year
- Month
- Month Name
- Year-Month
- Shipping Days
- Profit Status (Profit / Loss)

### Step 4: Business KPI Analysis

Calculated key business performance indicators:

- Total Sales
- Total Profit
- Total Quantity Sold
- Total Orders
- Total Customers
- Average Order Value
- Average Profit per Order
- Overall Profit Margin

### Step 5: Exploratory Data Analysis (EDA)

Performed business-focused analysis to answer questions such as:

- Which product category generates the highest sales?
- Which sub-categories generate the highest and lowest profits?
- Which region contributes the highest sales?
- Who are the top 10 customers by sales?
- Which months record the highest and lowest sales?
- How does sales performance change month over month?
- How do different discount levels affect profitability?
- Which orders generate negative profits?

### Step 6: Data Visualization

Created six visualizations using Matplotlib and Seaborn:

- Monthly Sales Trend – Line Chart
- Sales by Category – Bar Chart
- Profit by Sub-Category – Horizontal Bar Chart
- Sales by Region – Bar Chart
- Sales Distribution – Histogram
- Discount vs Profit – Scatter Plot

### Step 7: Report Generation

Exported the analysis into a multi-sheet Excel workbook containing:

- Cleaned Data
- KPI Summary
- Category Analysis
- Region Analysis
- Monthly Sales
- Subcategory Profit
- Monthly KPIs
- Top Customers
- Insights & Recommendations

## 5. Key Insights and Strategic Recommendations

### Key Insights

**1. Category Performance**
- Technology recorded the highest sales among the major product categories.
- Furniture generated considerable sales but had a relatively low profit margin.
- Technology demonstrated stronger profitability compared to Furniture.

**2. Sub-Category Profitability**
- Copiers, Phones, and Accessories were among the highest profit-generating sub-categories.
- Tables and Bookcases recorded negative profits.

**3. Regional Performance**
- The West region recorded the highest sales contribution.
- Regional analysis helped identify differences in sales and profitability.

**4. Discount Analysis**
- Higher discount levels, particularly 30% and above, were associated with profitability challenges.
- Excessive discounting can reduce overall business profitability.

**5. Monthly Sales Trends**
- Sales demonstrated seasonal patterns.
- September, November, and December were among the stronger sales periods.

**6. Loss-Making Orders**
- Identified orders with negative total profit that require further investigation.

### Strategic Recommendations

- **Optimize Discount Strategies:** Review high-discount transactions and evaluate appropriate discount limits to protect profitability.
- **Improve Furniture Profitability:** Reassess pricing and discount structures within the Furniture category.
- **Review Loss-Making Products:** Investigate supplier costs, pricing, and discount practices for Tables and Bookcases.
- **Focus on Profitable Categories:** Prioritize products with stronger profit margins when planning promotional activities.
- **Plan Seasonal Campaigns:** Prepare inventory and promotional strategies ahead of high-performing sales periods.
- **Monitor Loss-Making Orders:** Regularly investigate unprofitable orders to identify the reasons behind losses.

## 6. How to Run the Project

### Prerequisites
- Python 3.x
- Jupyter Notebook
- Required Python libraries

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the Project Folder

```bash
cd Sales-Data-Analysis-and-Business-Insights
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Jupyter Notebook

```bash
jupyter notebook
```

Open `Superstore_Sales.ipynb` and execute the notebook cells.

### Step 5: Run the Streamlit Application

```bash
streamlit run app.py
```

## 7. Future Scope

- Develop an interactive dashboard with additional filters and business KPIs.
- Integrate SQL for database storage and advanced querying.
- Perform customer segmentation using RFM analysis.
- Implement sales forecasting to estimate future business performance.
- Conduct deeper analysis of discount strategies and profit margins.
- Automate data updates and report generation.
- Enhance the application with more interactive business insights.

## 8. Contact & Professional Links

**Sharini G**  
Aspiring Data Analyst

- **LinkedIn:** www.linkedin.com/in/sharini-g-571546382
- **GitHub:** https://github.com/sharini16173
- **Email:**  g.sharini1601@gmail.com
