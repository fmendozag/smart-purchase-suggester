# 🧠 Smart Purchase Suggestion System

This project automates the process of generating **data-driven purchase recommendations** based on historical sales, stock levels, and supplier costs.  
It was developed as part of a real-world **Data Analysis & Optimization workflow**, integrating Python, SQL Server, and Excel reporting.

---

## 🚀 Project Overview

The system performs a complete analysis to determine **optimal purchase quantities** for each product by:

1. Reading data directly from a **SQL Server database**:
   - Sales history  
   - Purchase history  
   - Product catalog  
   - Packaging units and conversions  

2. Applying **forecasting techniques** (mean, rolling average, weighted average, trend-based) to estimate demand.

3. Generating **purchase suggestions** considering:
   - Current stock  
   - Forecasted demand for a configurable coverage period (e.g., 7, 15, 21, 30 days)  
   - Minimum safety stock  
   - Best supplier cost  
   - Packaging presentation (unit, pack, display, box, etc.)  

4. Automatically exporting the result to an **Excel report**, ready for decision-making.

---

## ⚙️ Technologies Used

- **Python** → Main programming language  
- **Pandas** → Data manipulation and transformation  
- **PyODBC** → SQL Server database connection  
- **IPython Widgets** → Interactive controls inside Jupyter Notebook  
- **Excel export (pandas.to_excel)** → Reporting layer  
- **SQL Server** → Data source for transactions and inventory  

---

## 📊 Key Features

- Automatic SQL extraction (no manual CSVs needed)  
- Forecast of sales trends with configurable method and coverage  
- Dynamic packaging rounding (e.g., 3 displays or 1 box based on suggested units)  
- Supplier name shortening (25 characters) for cleaner reporting  
- Automatic filtering of invalid packaging ("Neg.", "NEG X3", etc.)  
- Export to Excel with formatted and ready-to-share data  

---

## 🧩 Project Structure

smart-purchase-suggester/
├── data/
│   ├── packaging.csv
│   ├── products.csv
│   ├── purchases.csv 
│   └── sales.ipynb   
├── notebooks/
│   └── demand_analysis.ipynb
├── src/
│   ├── data_loader.py
│   ├── demand_forecast.py
│   ├── load_from_db.py
│   ├── purchase_suggester.py
│   ├── stock_manager.py
│   └── supplier_selector.py
├── README.md
└── requirements.txt