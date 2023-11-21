"""
This script is used to produce the following insight:

Merge history of a Git repository to determine the distribution of code merges across different days of the week.
It extracts and identifies the predominant days when code contributions occur.

This info can help testing teams align their testing efforts accordingly.

Usage:
python merge_activity.py

Provide the following inputs:
Enter the start date in YYYY-MM-DD format (eg: 2022-01-01)
Enter the end date in YYYY-MM-DD format (must be greater than start date) (eg: 2023-11-31)
Enter the repository path: local or remote GitHub repositories
(eg: qxf2/newsletter_automation)

- The script prompts for necessary inputs and
then fetches the merge activity report within the specified date range.
It displays the results in the form of a simple html page.

Outputs:
The merge activity count days/month in the repository based on the PR merge activity.
"""

import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.github_pr_data_extractor import PRDataExtractor
from modules.fetch_report_merge_activity import fetch_report

def get_inputs():
    """
    Prompts the user to enter a start date, end date, repository path,
    branch name, and file type extension
    and validates the inputs.

    Returns: A tuple containing the start date, end date, repository path,
    branch name, and file type.
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

    repo_name_input = input("Enter the repository name: ")

    
    return start_date_input, end_date_input, repo_name_input


def write_html_report(file_info_df, file_name):
    """
    Writes a DataFrame to an HTML report file.

    Args:
        df (DataFrame): The DataFrame containing the data to be written to the HTML report.
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
    except (FileNotFoundError, PermissionError) as error:
        print(f"An error occurred while writing the HTML report: {str(error)}")



if __name__ == "__main__":
    start_date, end_date, repo_path = get_inputs()
    github_api = PRDataExtractor(repo_path)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    merge_details= github_api.get_merged_pr_details(start_date,end_date)    
    weekly_report=fetch_report(merge_details)    
    write_html_report(weekly_report, "weekly_merge_report.html")
    



