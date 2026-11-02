# Sales Data Analysis and Business Insights System

## 🎯 Project Objective
This project transforms raw retail transaction data into strategic business intelligence. Bridging the gap between technical data manipulation and practical business administration, the system cleanses dataset inconsistencies, calculates high-level KPIs, and automates the generation of executive-ready PDF and Excel reports. The primary objective is to uncover profitability drivers, identify loss-making segments, and provide actionable, data-backed recommendations for retail growth.

## 🛠️ Skills and Technologies Showcased
* **Technical Stack:** Python (Pandas, Matplotlib, Seaborn, Openpyxl, ReportLab)
* **Data Processing:** Data Cleaning, Feature Engineering, Handling Missing Values, Date-Time Parsing
* **Analytics:** KPI Calculation (Average Order Value, Profit Margins), Cohort/Segment Analysis, Trend Identification
* **Reporting:** Automated Multi-sheet Excel Generation, Programmatic PDF Executive Summaries

## 📂 Repository Structure
* `/data` - Contains the raw CSV input files (e.g., `Sample - Superstore.csv`).
* `/notebooks` - Jupyter Notebooks detailing the exploratory data analysis (EDA) and pipeline logic.
* `/outputs` - Generated assets, including visualization `.png` files, Excel workbooks, and the final PDF report.
* `/scripts` - Python scripts designed to run the automated reporting pipeline.

## ⚙️ Analytical Workflow
1. **Data Ingestion:** Loaded the raw dataset, handling character encoding (latin1) to ensure data integrity.
2. **Data Cleansing:** Formatted column headers, converted string dates to `datetime` objects, calculated shipping durations, and engineered categorical profit flags (Profit vs. Loss).
3. **Metric Aggregation:** Grouped multidimensional data to isolate top-spending customers, evaluate category/sub-category performance, and map geographical sales distributions.
4. **Dashboard Generation:** Programmatically generated and exported distinct visualizations illustrating monthly trends, categorical sales, sub-category profitability, regional performance, and discount-to-profit ratios.
5. **Report Automation:** Exported cleaned data and KPI summaries into a structured `.xlsx` file and compiled a standalone PDF report embedding insights and visualizations.

## 📈 Key Insights and Strategic Recommendations

### Key Insights
* **The Discount Threshold:** Applying discounts of 30% or more consistently results in financial losses across all product categories.
* **Volume vs. Margin Mismatch:** The Furniture category drives massive sales volume but yields a critically low profit margin of just 2.49%.
* **Underperforming Segments:** Tables and Bookcases are actively loss-making sub-categories that drag down overall profitability.
* **Seasonal Peaks:** Sales volume demonstrates strong seasonality, consistently peaking during September, November, and December.

### Strategic Recommendations
* **Optimize Discounting:** Cap standard promotional discounts at a strict 20% ceiling to protect baseline profitability.
* **Pricing Overhaul:** Reevaluate supplier costs, pricing structures, and discount allowances specifically for Tables and Bookcases.
* **Margin Improvement:** Improve overall Furniture margins by raising baseline prices or heavily restricting markdowns.
* **Marketing Reallocation:** Direct Q4 promotional budgets toward Technology and Office Supplies, which carry the highest profit margins (above 17%).

## 🚀 How to Run the Project
1. Clone this repository to your local machine.
2. Ensure you have the required Python libraries installed: 
   `pip install pandas matplotlib seaborn openpyxl reportlab`
3. Verify that your raw data file is located in the `data/` directory.
4. Run the Jupyter Notebook or execute the Python script in the `scripts/` folder.
5. Review the generated charts, Excel workbook, and PDF report in the `outputs/` folder.

## 🔮 Future Scope
* **Interactive Dashboards:** Transition static Matplotlib charts into a live, interactive Power BI or Tableau dashboard.
* **Database Integration:** Replace the CSV ingestion step by querying the raw data directly from a SQL database (e.g., MySQL or PostgreSQL).
* **Predictive Forecasting:** Implement time-series forecasting (ARIMA or Prophet) to predict next year's Q4 sales volume.

## 📬 Contact
* **Name:** SHARINI G
* **LinkedIn:** www.linkedin.com/in/sharini-g-571546382
* **Email:** g.sharini1601@gmail.com
* **GitHub:** https://github.com/sharini16173
