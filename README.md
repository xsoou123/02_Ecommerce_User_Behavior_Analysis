# 🇧🇷 Brazil E-commerce User Behavior Analysis

An end-to-end business intelligence project based on the Brazilian Olist
E-commerce Dataset. The project covers raw data preparation, MySQL storage, SQL
business analysis, Python exploratory analysis, RFM customer segmentation, and
Tableau dashboard development.

![Dashboard preview](tableau/Dashboard.png)

## Project workflow

```text
Raw CSV data
      ↓
Python data import
      ↓
MySQL database
      ↓
SQL business analysis
      ↓
Python EDA and RFM segmentation
      ↓
Tableau dashboard and business insights
```

## Repository contents

| Section | Description |
| --- | --- |
| [`data/raw`](data/raw) | Original Olist CSV datasets |
| [`data/processed`](data/processed) | Processed customer segmentation data |
| [`mysql`](mysql) | Database schema and import SQL |
| [`python`](python) | Data import, EDA, and result-export scripts |
| [`sql`](sql) | Business analysis queries and views |
| [`report`](report) | Generated CSV analysis results |
| [`tableau`](tableau) | Tableau workbooks and dashboard preview |

## Business questions

- How do sales and order volumes change over time?
- Which product categories and products generate the most revenue?
- Where are customers geographically concentrated?
- Which payment methods are most important?
- Which customers are high-value, loyal, or newly acquired?
- How many customers make repeat purchases?

## Technology

- Python, pandas, SQLAlchemy, and PyMySQL
- MySQL and SQL
- Tableau
- Git and GitHub

## Run the project locally

### 1. Install Python dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Configure MySQL

Create the database and tables with
[`mysql/create_tables.sql`](mysql/create_tables.sql). Then copy the example
configuration:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace `replace_with_your_password` with your local MySQL
password. The `.env` file is excluded from Git and must never be committed.

### 3. Import and analyze the data

Run these commands from the project root:

```powershell
python .\python\01_import_mysql.py
python .\python\02_eda_analysis.py
```

After creating the SQL views in
[`sql/03_sql_analysis.sql`](sql/03_sql_analysis.sql), export their results:

```powershell
python .\python\03_export_sql_result.py
```

All scripts use paths relative to the repository, so the project can be cloned
and run from any local directory.

## Main analysis outputs

- KPI summary: customers, orders, GMV, and average order value
- Monthly sales trend
- Product and category performance
- Customer geographic distribution
- Payment-method analysis
- Repeat-purchase analysis
- RFM customer segmentation

The generated result files are available in [`report`](report) and
[`report/sql_result`](report/sql_result).

## Tableau dashboard

The dashboard includes KPI cards, monthly sales trends, category performance,
regional customer distribution, payment analysis, and RFM customer segments.

- [Dashboard image](tableau/Dashboard.png)
- [Tableau workbook](tableau/Brazil_Ecommerce_Dashboard.twb)

GitHub can preview the dashboard image. To use filters and other interactive
features, open the workbook in Tableau or publish it separately to Tableau
Public.

## Dataset

This project uses the public Olist Brazilian E-commerce Dataset, including
orders, order items, customers, products, payments, reviews, sellers,
geolocation, and product-category translation data.

The geolocation CSV is approximately 58 MB. GitHub permits it in a normal Git
repository but may not render the complete table in the browser; the file
remains available for download.

## Portfolio highlights

- End-to-end ETL and database workflow
- Multi-table SQL analysis
- Business KPI design
- Exploratory data analysis
- RFM customer segmentation
- Tableau dashboard design
- Reproducible configuration without committed credentials

## Author

Data analyst portfolio project built with Python, SQL, MySQL, and Tableau.
