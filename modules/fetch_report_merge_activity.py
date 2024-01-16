"""
This script collects merge activity data
"""

import pandas as pd

def get_merge_activity_details(merge_activity_df):
    """
    Analyzes merge activity data and provides insights.

    Parameters:
    - merge_activity_df (DataFrame): DataFrame containing merge activity data.

    Returns:
    - analyzed_df (DataFrame): DataFrame with detailed analysis results.
    """

    merge_activity_df['created_at'] = pd.to_datetime(merge_activity_df['created_at'])
    merge_activity_df['closed_at'] = pd.to_datetime(merge_activity_df['closed_at'])

    merge_activity_df['day_of_week'] = merge_activity_df['closed_at'].dt.dayofweek
    merge_activity_df['month'] = merge_activity_df['closed_at'].dt.strftime('%Y-%B')

    grouped_by_month_day = merge_activity_df.groupby(['month', 'day_of_week']).size()
    monthly_day_of_week_counts = grouped_by_month_day.unstack(fill_value=0)

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

    #Find and display insights

    row_max = analyzed_df[analyzed_df['Merges'] == analyzed_df['Merges'].max()]
    max_months = row_max['Month'].tolist()
    max_day_of_week = row_max['Day_of_Week'].tolist()
    merge_count = row_max['Merges'].max()

    day_month_dict = {}
    # Use enumerate instead of range and len
    for i, day in enumerate(max_day_of_week):
        day_month = day + ", " + max_months[i]
        day_month_dict[day_month] = merge_count
    
    print("\nInsights for the timeperiod :")

    print(f"\nThe maximum number of merges during the specified period was: {merge_count}")

    print("\nThese occured on the following days of the week:")
    for key, value in day_month_dict.items():
        print(f"   -> {key}: {value}")

    print('\nDetailed report can be found in merge_activity_report.html\n')

    return analyzed_df
