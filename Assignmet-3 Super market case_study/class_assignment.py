import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# # Question no # 1 Answer :

df = pd.read_csv("supermarket_sales_case_study.csv")
original_rows =len(df)
audit_trail= []
def record_audit(step, rows_before, rows_after):
    audit_trail.append({
        'Step': step,
        'Rows before': rows_before,
        'Rows after': rows_after,
        'Rows removed': rows_before - rows_after
    })  
print(df.shape)
print(df.head())
print(df.dtypes)

# # Question no # 2 Answer :
rows_before = len(df)

print(df.isnull().sum())
print(df.duplicated().sum())

invoice_count=(df['Invoice ID'].value_counts())
shared_ids=((invoice_count[invoice_count>1]))
print(len(shared_ids))
print(shared_ids)

print(df['Gender'].unique())
print(df['Payment'].unique())

record_audit('Standardize text columns', rows_before, len(df))

# #  Question no # 3 Answer :

rows_before = len(df)
df = df.drop_duplicates()
record_audit('Remove exact duplicates', rows_before, len(df))

# #  Question no # 4 Answer :

rows_before = len(df)

df = df.drop_duplicates(subset=['Invoice ID'], keep='last')

record_audit('Remove duplicate Invoice IDs', rows_before, len(df))
#  #  Question no # 5 Answer :
rows_before = len(df)

df['Gender']=df['Gender'].str.strip().str.lower()
df['Payment']=df['Payment'].str.strip().str.lower()

df['Gender']=df['Gender'].map({
    'male':'Male',
    'female':'Female'
 })
df['Payment']=df['Payment'].map({
    'cash':'Cash',
    'credit card':'Credit card',
    'ewallet':'Ewallet'
 })

print(df['Gender'].unique())
print(df['Payment'].unique())

record_audit('Standardize Gender and Payment', rows_before, len(df))

#  #  Question no # 6 Answer :
rows_before = len(df)

print("Negative Quantities befor cleaning",(df['Quantity']<0).sum())
df['Quantity']=df['Quantity'].abs()
print("Negative Quantities befor cleaning",(df['Quantity']<0).sum())

record_audit('Correct negative quantities', rows_before, len(df))

#  #  Question no # 7 Answer :
rows_before = len(df)

original_dates=df['Date'].copy()

df['Date']=pd.to_datetime(original_dates,
    format='%m/%d/%Y',
    errors='coerce')

missing = df['Date'].isna()

df.loc[missing, 'Date'] = pd.to_datetime(
    original_dates[missing],
    format='%d-%m-%Y',
    errors='coerce'
)

# Check the results
print(df['Date'].head())
print("Missing dates after both attempt:", df['Date'].isna().sum())

print(original_dates[df['Date'].isna()].value_counts(dropna=False))

record_audit('Parse mixed date formats  ', rows_before, len(df))

#  #  Question no # 8 Answer :
rows_before = len(df)


original_column= df['Total'].copy()

expected_total=df['Quantity']*df['Unit price']*1.05
difference= abs(expected_total-df['Total'])

wrong_total= difference>0.50

df.loc[wrong_total,'Total'] = expected_total[wrong_total]


print("rows corrected",wrong_total.sum())
print(df.loc[wrong_total,'Total'])

record_audit('Correct incorrect totals', rows_before, len(df))
#  #  Question no # 9 Answer :
rows_before = len(df)

print("befor replacing",df['Customer type'].value_counts(dropna=False))
df['Customer type']=df['Customer type'].fillna('Unknown')
print("After replacing",df['Customer type'].value_counts(dropna=False))

print("Before replacing mean",df['Rating'].isna().sum())
median_rating=df['Rating'].median()
print(median_rating)

df['Rating']=df['Rating'].fillna(median_rating)
print("After replacing mean",df['Rating'].isna().sum()) 

record_audit(
    'Fill missing Customer type and Rating',
    rows_before,
    len(df))

rows_before = len(df)

df = df.dropna(subset=['Date'])

record_audit('Drop rows with missing Date', rows_before, len(df))

#  #  Question no # 10 Answer :

audit_df = pd.DataFrame(audit_trail)

print("\nAudit Trail:")
print(audit_df.to_string(index=False))

print("\nOriginal row count:", original_rows)
print("Final row count:", len(df))
print("Total rows removed:", original_rows - len(df))


# ==========================================================
# Q1. ADD TIME COLUMNS
# ==========================================================

# Make sure Date is in datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Convert Time to datetime so we can extract the hour
parsed_time = pd.to_datetime(
    df['Time'].astype(str),
    format='%H:%M',
    errors='coerce'
)

df['Year'] = df['Date'].dt.year
df['Quarter'] = df['Date'].dt.to_period('Q').astype(str)
df['Day of week'] = df['Date'].dt.day_name()
df['Hour'] = parsed_time.dt.hour

print("\nQ1: Time columns added")
print(df[['Date', 'Time', 'Year', 'Quarter',
          'Day of week', 'Hour']].head())


# ==========================================================
# Q2. BUCKET THE TRADING DAY
# Morning:   10:00–12:59 (3 hours)
# Afternoon: 13:00–16:59 (4 hours)
# Evening:   17:00–20:59 (4 hours)
# ==========================================================

conditions = [
    df['Hour'].between(10, 12),
    df['Hour'].between(13, 16),
    df['Hour'].between(17, 20)
]

buckets = ['Morning', 'Afternoon', 'Evening']

df['Trading period'] = np.select(
    conditions,
    buckets,
    default='Outside trading hours'
)

# Count transactions per branch and trading period
period_hours = {
    'Morning': 3,
    'Afternoon': 4,
    'Evening': 4
}

trading_summary = (
    df[df['Trading period'].isin(buckets)]
    .groupby(['Branch', 'Trading period'])
    .size()
    .reset_index(name='Transactions')
)

trading_summary['Hours in bucket'] = (
    trading_summary['Trading period'].map(period_hours)
)

trading_summary['Transactions per hour'] = (
    trading_summary['Transactions'] /
    trading_summary['Hours in bucket']
)

print("\nQ2: Transactions per hour")
print(trading_summary)


# ==========================================================
# Q3. QUARTERLY REVENUE AND TARGET COMPARISON
# Target = $100,000 per branch per quarter
# ==========================================================

quarterly_revenue = (
    df.dropna(subset=['Quarter', 'Branch', 'Total'])
    .groupby(['Branch', 'Quarter'])['Total']
    .sum()
    .reset_index(name='Revenue')
)

# Create a target for every branch
branches = sorted(df['Branch'].dropna().unique())

targets = pd.DataFrame({
    'Branch': branches,
    'Target': [100000] * len(branches)
})

# Join quarterly revenue with targets
quarterly_comparison = quarterly_revenue.merge(
    targets,
    on='Branch',
    how='left'
)

quarterly_comparison['Variance'] = (
    quarterly_comparison['Revenue'] -
    quarterly_comparison['Target']
)

quarterly_comparison['% of target'] = (
    quarterly_comparison['Revenue'] /
    quarterly_comparison['Target'] * 100
)

quarterly_comparison['Hit'] = (
    quarterly_comparison['Revenue'] >=
    quarterly_comparison['Target']
)

print("\nQ3: Quarterly revenue vs target")
print(quarterly_comparison)


# ==========================================================
# Q4. SUMMARISE EACH BRANCH
# Average quarterly revenue, quarters hit, best/worst
# quarter, and YoY growth
# ==========================================================

# Define the eight quarters in chronological order
quarters = [
    '2023Q1', '2023Q2', '2023Q3', '2023Q4',
    '2024Q1', '2024Q2', '2024Q3', '2024Q4'
]

# Create a complete branch-by-quarter revenue table.
# Missing branch-quarter combinations are treated as zero.
revenue_table = (
    quarterly_comparison
    .pivot(index='Branch', columns='Quarter', values='Revenue')
    .reindex(index=branches, columns=quarters)
    .fillna(0)
)

# Number of quarters meeting the target, out of 8
hit_table = (
    quarterly_comparison
    .pivot(index='Branch', columns='Quarter', values='Hit')
    .reindex(index=branches, columns=quarters)
    .fillna(False)
    .astype(bool)
)

branch_summary = pd.DataFrame(index=branches)

branch_summary['Average quarterly revenue'] = (
    revenue_table.mean(axis=1)
)

branch_summary['Quarters hit out of 8'] = (
    hit_table.sum(axis=1)
)

branch_summary['Best quarter'] = (
    revenue_table.idxmax(axis=1)
)

branch_summary['Best quarter revenue'] = (
    revenue_table.max(axis=1)
)

branch_summary['Worst quarter'] = (
    revenue_table.idxmin(axis=1)
)

branch_summary['Worst quarter revenue'] = (
    revenue_table.min(axis=1)
)

# Total revenue in each year
revenue_2023 = revenue_table[
    ['2023Q1', '2023Q2', '2023Q3', '2023Q4']
].sum(axis=1)

revenue_2024 = revenue_table[
    ['2024Q1', '2024Q2', '2024Q3', '2024Q4']
].sum(axis=1)

branch_summary['YoY growth %'] = np.where(
    revenue_2023 != 0,
    (revenue_2024 / revenue_2023 - 1) * 100,
    np.nan
)

branch_summary = branch_summary.reset_index(
    names='Branch'
)

print("\nQ4: Branch summary")
print(branch_summary)


# ==========================================================
# Q5. FIND THE BUSY TIMES
# Average transactions per day for each weekday
# ==========================================================

# Count unique dates in the dataset for each weekday
weekday_dates = (
    df.dropna(subset=['Date'])
    .drop_duplicates(subset=['Date'])[['Date', 'Day of week']]
)

weekday_days = (
    weekday_dates.groupby('Day of week')['Date']
    .nunique()
)

weekday_order = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday',
    'Friday', 'Saturday', 'Sunday'
]

weekday_transactions = (
    df.dropna(subset=['Day of week'])
    .groupby('Day of week')
    .size()
    .reindex(weekday_order, fill_value=0)
)

weekday_average = (
    weekday_transactions /
    weekday_days.reindex(weekday_order).replace(0, np.nan)
)

print("\nQ5: Average transactions per weekday")
print(weekday_average)

# Average transactions for each hour of each weekday
valid_hours = df[
    df['Hour'].between(10, 20) &
    df['Day of week'].notna()
].copy()

hourly_counts = (
    valid_hours.groupby(['Day of week', 'Hour'])
    .size()
    .unstack(fill_value=0)
    .reindex(index=weekday_order, columns=range(10, 21),
             fill_value=0)
)

# Divide by the number of dates for each weekday
hourly_average = hourly_counts.div(
    weekday_days.reindex(weekday_order).replace(0, np.nan),
    axis=0
)

print("\nQ5: Average transactions by weekday and hour")
print(hourly_average)


# Improved heatmap: highlight peak trading times

fig, ax = plt.subplots(figsize=(13, 6))

# Keep missing values as missing instead of displaying them as zero
heatmap_data = hourly_average

# Warm colors make busier periods stand out
im = ax.imshow(
    heatmap_data.values,
    aspect='auto',
    cmap='YlOrRd',
    interpolation='nearest'
)

# Add hour and weekday labels
ax.set_xticks(range(len(heatmap_data.columns)))
ax.set_xticklabels(heatmap_data.columns)

ax.set_yticks(range(len(heatmap_data.index)))
ax.set_yticklabels(heatmap_data.index)

ax.set_xlabel('Hour of Day', fontsize=11)
ax.set_ylabel('Day of Week', fontsize=11)
ax.set_title(
    'Supermarket Peak Trading Times',
    fontsize=15,
    fontweight='bold',
    pad=15
)

# Add a thin white grid between cells
ax.set_xticks(
    np.arange(-0.5, len(heatmap_data.columns), 1),
    minor=True
)
ax.set_yticks(
    np.arange(-0.5, len(heatmap_data.index), 1),
    minor=True
)
ax.grid(which='minor', color='white', linestyle='-', linewidth=1.5)
ax.tick_params(which='minor', bottom=False, left=False)

# Display average transaction values inside each cell
values = heatmap_data.values
peak_value = np.nanmax(values)

for i in range(values.shape[0]):
    for j in range(values.shape[1]):
        value = values[i, j]

        if not np.isnan(value):
            # Use contrasting text for readability
            text_color = 'white' if value > peak_value * 0.55 else 'black'

            ax.text(
                j, i, f'{value:.2f}',
                ha='center',
                va='center',
                fontsize=8,
                color=text_color
            )

# Color scale
cbar = fig.colorbar(im, ax=ax, pad=0.02)
cbar.set_label('Average Transactions per Day', fontsize=10)

plt.tight_layout()
plt.savefig('weekday_hour_heatmap.png', dpi=200, bbox_inches='tight')
plt.show()
plt.close()


# ==========================================================
# Q6. CHART, EXPORT, AND MANAGEMENT SUMMARY
# ==========================================================

# Plot quarterly revenue for each branch
for branch in branches:
    plt.figure(figsize=(10, 5))

    plt.plot(
        quarters,
        revenue_table.loc[branch, quarters].values,
        marker='o',
        label='Quarterly revenue'
    )

    plt.axhline(
        y=100000,
        linestyle='--',
        label='Target: $100,000'
    )

    plt.title(f'Quarterly Revenue - Branch {branch}')
    plt.xlabel('Quarter')
    plt.ylabel('Revenue')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    filename = f"branch_{branch}_quarterly_revenue.png"
    plt.savefig(filename, dpi=150)
    plt.show()
    plt.close()

# Export cleaned data
df.to_csv('supermarket_cleaned.csv', index=False)

# Export analytical results too
quarterly_comparison.to_csv(
    'quarterly_target_comparison.csv', index=False
)

branch_summary.to_csv(
    'branch_summary.csv', index=False
)

trading_summary.to_csv(
    'trading_period_summary.csv', index=False
)

hourly_average.to_csv('weekday_hour_averages.csv')

print("\nQ6: Files exported successfully.")


# Five-line management summary
print("\nMANAGEMENT SUMMARY")

best_branch = branch_summary.loc[
    branch_summary['Average quarterly revenue'].idxmax()
]

print(
    f"1. Highest average quarterly revenue: "
    f"Branch {best_branch['Branch']} "
    f"(${best_branch['Average quarterly revenue']:,.2f})."
)

most_hits = branch_summary.loc[
    branch_summary['Quarters hit out of 8'].idxmax()
]

print(
    f"2. Most target-hit quarters: Branch {most_hits['Branch']} "
    f"({int(most_hits['Quarters hit out of 8'])} out of 8)."
)

best_growth = branch_summary.dropna(
    subset=['YoY growth %']
)

if not best_growth.empty:
    growth_branch = best_growth.loc[
        best_growth['YoY growth %'].idxmax()
    ]

    print(
        f"3. Highest year-over-year growth: "
        f"Branch {growth_branch['Branch']} "
        f"({growth_branch['YoY growth %']:.2f}%)."
    )
else:
    print("3. Year-over-year growth could not be calculated.")

total_revenue = quarterly_revenue['Revenue'].sum()

print(
    f"4. Total recorded revenue across available quarters: "
    f"${total_revenue:,.2f}."
)

total_hits = int(quarterly_comparison['Hit'].sum())

print(
    f"5. Branch-quarter targets met: {total_hits} "
    f"out of {len(quarterly_comparison)} recorded branch-quarter results."
)
