
import pandas as pd
from collections import Counter

def fetch_report(merge_activity_df):
    "Fetching the montly weekly reports for merge activity"

    merge_activity_df['created_at'] = pd.to_datetime(merge_activity_df['created_at'])
    merge_activity_df['closed_at'] = pd.to_datetime(merge_activity_df['closed_at'])
   
    merge_activity_df['day_of_week'] = merge_activity_df['closed_at'].dt.dayofweek
    merge_activity_df['month'] = merge_activity_df['closed_at'].dt.strftime('%Y-%B')
    
    monthly_day_of_week_counts = merge_activity_df.groupby(['month', 'day_of_week']).size().unstack(fill_value=0)

    # Define the days of the week for display
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    analyzed_data = []
    for month, data in monthly_day_of_week_counts.iterrows():
        for day, count in data.items():
            analyzed_data.append({
            "Month": month,
            "Day_of_Week": days_of_week[day],
            "Merges": count
        })
    analyzed_df = pd.DataFrame(analyzed_data)

    #Find the insight from the report 
    row_max = analyzed_df[analyzed_df['Merges'] == analyzed_df['Merges'].max()]

    # Extract information from the row
    max_month = row_max['Month'].values[0]
    max_day_of_week = row_max['Day_of_Week'].values[0]
    merge_count = row_max['Merges'].values[0]
    print(f"Maximum merge happened on {max_day_of_week} in the month {max_month} : {merge_count}")
    return analyzed_df