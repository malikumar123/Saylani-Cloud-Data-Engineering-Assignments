# Supermarket Sales Analysis & Business Case Study

A Python and pandas project that cleans supermarket sales data, analyzes branch performance, evaluates quarterly revenue targets, and identifies busy trading periods using data visualization.

## Project Overview

This project was completed as part of a my SMIT course Cloud Data Engineerig. It demonstrates how raw sales data can be cleaned, transformed, analyzed, and converted into useful business insights.

The analysis covers three supermarket branches (A, B, and C) across eight quarters from 2023 Q1 to 2024 Q4.

## Objectives

- Clean missing, duplicated, and inconsistent data.
- Standardize transaction dates and categorical values.
- Correct negative quantities and inaccurate transaction totals.
- Maintain an audit trail of row counts and removed records.
- Compare quarterly branch revenue against a $100,000 target.
- Summarize branch performance and year-over-year growth.
- Identify busy weekdays and hourly trading periods.
- Generate charts, CSV reports, and management recommendations.

## Technologies Used

- **Python** — programming and analysis
- **pandas** — data cleaning and tabular analysis
- **NumPy** — numerical calculations
- **Matplotlib** — charts and heatmap visualization
- **CSV** — input data and exported results

## Project Files

| File | Description |
|---|---|
| `class_assignment.py` | Main data-cleaning and analysis script |
| `supermarket_cleaned.csv` | Cleaned dataset |
| `quarterly_target_comparison.csv` | Branch revenue, targets, variance, and target status |
| `branch_summary.csv` | Average revenue, target-hit quarters, best/worst quarter, and growth |
| `trading_period_summary.csv` | Transactions per hour by branch and trading period |
| `weekday_hour_averages.csv` | Average transactions by weekday and hour |
| `weekday_hour_heatmap.png` | Visualization of busy trading times |
| `branch_A_quarterly_revenue.png` | Quarterly revenue chart for Branch A |
| `branch_B_quarterly_revenue.png` | Quarterly revenue chart for Branch B |
| `branch_C_quarterly_revenue.png` | Quarterly revenue chart for Branch C |

## Methodology

### 1. Data Cleaning

The dataset was inspected for missing values, exact duplicate rows, repeated invoice IDs, inconsistent category values, negative quantities, mixed date formats, and incorrect totals. Missing customer types were filled with `Unknown`, missing ratings with the median, and rows with invalid dates were removed.

### 2. Time-Based Analysis

Year, quarter, day of week, and hour were extracted from the transaction date and time. Transactions were grouped into:

- Morning: 10:00–13:00
- Afternoon: 13:00–17:00
- Evening: 17:00–21:00

### 3. Quarterly Revenue Analysis

Revenue was compared against a target of $100,000 per branch per quarter. The analysis calculated revenue variance, percentage of target achieved, and whether each branch met its target.

### 4. Branch Performance

The project calculated average quarterly revenue, quarters meeting the target, best and worst quarters, and year-over-year growth.

### 5. Busy Trading Times

Average transaction counts were calculated for each weekday and hour. A heatmap was generated to help identify periods with higher transaction activity.

## Key Findings

Based on the analysis output:

- Branch A had the highest average quarterly revenue, approximately **$104,053.75**.
- Branch A met the target in **4 out of 8 quarters**.
- Branch B met the target in **2 out of 8 quarters**.
- Branch C had the highest year-over-year growth, approximately **8.14%**.
- **10 out of 24** recorded branch-quarter results met the $100,000 target.
- The heatmap highlighted Friday evening and Saturday around noon as busy periods.

## How to Run

1. Install Python.
2. Install the required libraries:

   ```bash
   pip install pandas numpy matplotlib
   ```

3. Place `class_assignment.py` and `supermarket_sales_case_study.csv` in the same directory.
4. Run the script:

   ```bash
   python class_assignment.py
   ```

The script generates cleaned data, analysis CSV files, quarterly revenue charts, a weekday/hour heatmap, and a management summary.

## Business Recommendations

- Investigate the factors contributing to Branch C's year-over-year growth.
- Review Branch B's lower target-hit rate and identify opportunities for improvement.
- Use observed peak trading periods to inform staffing reviews.
- Monitor quarterly revenue against the target and investigate underperforming quarters.

## Learning Outcomes

This project provided practical experience with data cleaning, pandas transformations, grouping and aggregation, date/time analysis, revenue calculations, CSV exports, and data visualization.

## Author

University coursework project — Python Data Analysis / Supermarket Sales Case Study.