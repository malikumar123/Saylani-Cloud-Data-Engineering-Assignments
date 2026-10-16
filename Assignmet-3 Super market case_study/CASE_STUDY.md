# Supermarket Sales Case Study

## 1. Introduction

Retail businesses collect sales transactions every day, but raw data may contain duplicate records, missing values, inconsistent formats, and incorrect calculations. These issues can affect the accuracy of business reports and decisions.

This project analyzes supermarket sales data for three branches: A, B, and C. The purpose is to clean the data, evaluate quarterly revenue performance, identify busy trading periods, and present findings that may help management make informed decisions.

The project uses Python, pandas, NumPy, and Matplotlib.

## 2. Business Problem

Management needs to understand three main questions:

1. Which branches are performing well against their quarterly revenue targets?
2. Which branches and quarters require further investigation?
3. When are transaction volumes highest, and how can this information support staffing decisions?

The analysis uses a target of $100,000 per branch per quarter.

## 3. Data Cleaning

The original dataset was inspected using pandas to identify missing values, duplicate rows, repeated invoice IDs, inconsistent categorical values, negative quantities, mixed date formats, and incorrect totals.

### 3.1 Duplicate Records

Exact duplicate rows were removed. Repeated invoice IDs were then handled according to the assignment instruction to retain the later record when an invoice ID appeared more than once.

### 3.2 Standardizing Categories

Gender and payment values were standardized to consistent labels. This makes grouping and reporting more reliable.

### 3.3 Correcting Quantities and Totals

Negative quantities were converted to absolute values because the assignment specified that the negative sign was a typing error.

Expected totals were calculated using:

**Expected Total = Quantity × Unit Price × 1.05**

If the difference between the expected total and recorded total exceeded $0.50, the recorded total was replaced with the calculated amount.

### 3.4 Handling Dates and Missing Values

Two date formats were attempted: month/day/year and day-month-year. Values that could not be parsed remained missing. Missing customer types were filled with `Unknown`, and missing ratings were filled with the median rating. Rows with missing dates were removed because they could not be assigned to a quarter.

### 3.5 Audit Trail

The audit trail records the row count before and after cleaning steps and calculates the number of rows removed.

The reported counts were:

| Measure | Rows |
|---|---:|
| Original dataset | 8,631 |
| Removed exact duplicate rows | 30 |
| Removed additional duplicate invoice rows | 25 |
| Removed rows with missing dates | 17 |
| Final dataset | 8,559 |
| Total rows removed | 72 |

The total reduction was 72 rows. These counts should be checked against the final run of the script before submission.

## 4. Methodology

### 4.1 Time-Based Columns

The transaction date and time were used to create four additional columns:

- Year
- Quarter, such as `2023Q1`
- Day of week
- Hour

These columns allow transactions to be grouped by reporting period and trading time.

### 4.2 Trading Period Analysis

The trading day was divided into three periods:

| Period | Time range | Hours |
|---|---|---:|
| Morning | 10:00–13:00 | 3 |
| Afternoon | 13:00–17:00 | 4 |
| Evening | 17:00–21:00 | 4 |

Transactions were counted by branch and trading period. The count was divided by the number of hours in the period to calculate transactions per hour.

### 4.3 Quarterly Revenue and Target Comparison

Revenue was summed by branch and quarter. Each branch-quarter result was compared with the $100,000 target.

The calculations were:

- **Variance = Revenue − Target**
- **Percentage of Target = Revenue ÷ Target × 100**
- **Target Hit = Revenue is at least $100,000**

A positive variance indicates that the target was exceeded, while a negative variance indicates that revenue was below target.

### 4.4 Branch Performance Summary

The analysis calculated each branch's average quarterly revenue, number of quarters meeting the target, best quarter, worst quarter, and year-over-year growth.

Year-over-year growth was calculated using:

**YoY Growth (%) = (2024 Revenue ÷ 2023 Revenue − 1) × 100**

### 4.5 Weekday and Hour Analysis

The average number of transactions per weekday was calculated by dividing transactions on that weekday by the number of occurrences of that weekday in the dataset.

The same method was applied to each hour of each weekday. The results were visualized in a heatmap, with stronger colors indicating higher average transaction activity.

## 5. Results and Findings

### 5.1 Branch Performance

The analysis output reported the following findings:

- Branch A had the highest average quarterly revenue at approximately $104,053.75.
- Branch A met the target in 4 out of 8 quarters.
- Branch B met the target in 2 out of 8 quarters.
- Branch C had the highest year-over-year growth at approximately 8.14%.
- Across 24 recorded branch-quarter results, 10 met the $100,000 target.

These results suggest that branch performance differed across the two-year period. Branch B's lower target-hit count may warrant further investigation, while Branch C's growth may provide useful lessons for the other branches.

### 5.2 Busy Trading Periods

The weekday/hour heatmap highlighted higher average transaction activity around Friday at 18:00 and Saturday around noon.

These patterns can help management identify periods to investigate when planning staff schedules. However, transaction counts alone do not establish the ideal staffing level; customer service requirements and the length of queues should also be considered.

### 5.3 Revenue Target Performance

Quarterly revenue comparisons show which branch-quarter results exceeded the target and which fell short. This provides a structured basis for reviewing performance and identifying quarters requiring further analysis.

## 6. Management Recommendations

Based on the analysis, the following actions are recommended:

1. **Review Branch B's performance.** Investigate the reasons for its lower number of target-hit quarters, such as product mix, sales volume, or local customer demand.
2. **Study Branch C's growth.** Compare its performance across years and identify practices that may be useful to other branches.
3. **Review staffing at peak times.** Examine Friday evenings and Saturday around noon when planning staffing, and validate the patterns against operational observations.
4. **Monitor quarterly targets.** Review revenue variance regularly and investigate the reasons for significant shortfalls.
5. **Maintain data quality.** Continue checking duplicates, invalid dates, missing values, and inconsistent totals before preparing business reports.

These are recommendations for further investigation, not proof of the causes behind the observed sales patterns.

## 7. Deliverables

The GitHub project contains the Python analysis script, cleaned dataset, quarterly target comparison, branch summary, trading-period summary, weekday/hour averages, weekday/hour heatmap, and quarterly revenue charts.

## 8. Limitations

The findings depend on the accuracy and coverage of the supplied dataset. Missing or invalid dates cannot be assigned to quarters, and corrections made under the assignment rules may differ from the original business records.

The analysis identifies transaction patterns and revenue performance but does not establish why a branch performed well or poorly. Further investigation would be needed to test possible explanations.

## 9. Conclusion

This case study demonstrates how Python can be used to transform raw supermarket sales records into structured and useful business information. Data cleaning improved consistency, quarterly target comparisons highlighted differences between branches, and the heatmap made busy trading periods easier to identify.

The project provides a foundation for ongoing sales monitoring and further business analysis.   