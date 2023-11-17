"""
This script is used to produce the following insight:
Find the average PR review time within the specified time period
This info can help testing teams align their testing efforts accordingly.

Usage:
python pr_review_time.py

Provide the following inputs:
Enter the start date in YYYY-MM-DD format (eg: 2023-02-01)
Enter the end date in YYYY-MM-DD format (must be greater than start date) (eg: 2023-02-08)
Enter the repository name: local or remote GitHub repositories
(eg: qxf2/newsletter_automation)

- The script prompts for necessary inputs and
then fetches the PR details and calculates the average review time within the specified date range.
It displays the results in the form of a simple html page.

Outputs:
The average time take for PR review for the specified time period.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.pr_review_time import calculate_review_time
import pandas as pd
from datetime import datetime

def get_inputs():
    """
    Prompts the user to enter a start date, end date, repository name

    Returns: A tuple containing the start date, end date, repository name
    """

    while True:
        try:
            start_date_input = input("Enter the start date (YYYY-MM-DD): ")
            start_date_input = datetime.strptime(start_date_input, "%Y-%m-%d")
            break
        except ValueError:
            print(
                "Invalid start date format. Please enter a valid date in YYYY-MM-DD format."
            )

    while True:
        try:
            end_date_input = input("Enter the end date (YYYY-MM-DD): ")
            end_date_input = datetime.strptime(end_date_input, "%Y-%m-%d")
            if end_date_input > start_date_input:
                break
            print("End date must be greater than start date. Please try again.")

        except ValueError:
            print("Invalid date format. Please try again.")
    
    start_date_input=start_date_input.strftime('%Y-%m-%d')
    end_date_input=end_date_input.strftime('%Y-%m-%d')
    repo_name = input("Enter the repository name: ")

    return start_date_input, end_date_input, repo_name

def draw_inference(review_details):
    # Calculate the average review time
    average_review_time = review_details['review_time'].mean()

    # Identify PRs with review times longer than the average
    long_review_prs = review_details[review_details['review_time'] > average_review_time]

    # Display average review time
    print(f"Average Review Time: {average_review_time}")

    # Display information about PRs with long review times
    if not long_review_prs.empty:
        print("PRs with longer than average review time:")
        for index, row in long_review_prs.iterrows():
            print(f"PR #{row['pr_number']}: {row['pr_title']} - Review Time: {row['review_time']}")
         
    return average_review_time,long_review_prs 
     
def write_html_report(file_info_df, review_time, long_review_prs ,file_name):
    """
    Writes the DataFrame and average review time to an HTML report file.

    Args:
        file_info_df: The DataFrame containing the data to be written to the HTML report.
        review_time: Average PR review time to be written to the html report
        file_name (str): The name of the file to which the HTML report will be written.

    Returns:
        None
    """
    try:
        with open(file_name, "w", encoding='utf-8') as file:
            if file_info_df.empty:
                message = "No data available between the specified dates."
                file.write(message)
            else:
                html = file_info_df.to_html(index=False)
                file.write(html)
                file.write("Average PR review time:" + str(review_time))
    except (FileNotFoundError, PermissionError) as error:
        print(f"An error occurred while writing the HTML report: {str(error)}")

if __name__ == "__main__":
    start_date, end_date, repo_name = get_inputs()
    review_details = calculate_review_time(repo_name,start_date,end_date)
    average_review_time,long_review_prs = draw_inference(review_details)
    write_html_report(review_details,average_review_time,long_review_prs,"pr_review_time_report.html")
