"""
This script is used to produce the following insight:

Merge history of a Git repository to determine the distribution of code merges 
across different days of the week.
It extracts and identifies the predominant days when code contributions occured.

Usage:
python merge_activity.py

Provide the following inputs:
Enter the start date in YYYY-MM-DD format (eg: 2022-01-01)
Enter the end date in YYYY-MM-DD format (must be greater than start date) (eg: 2023-11-31)
Enter the repository path: local or remote GitHub repositories
(eg: qxf2/newsletter_automation)

- The script prompts for necessary inputs and
then fetches the merge activity report within the specified date range.
It displays inference based on the data fetched and a simple html report.
"""

import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.github_pr_data_extractor import PRDataExtractor, PRDataExtractionError
from modules.fetch_report_merge_activity import get_merge_activity_details
from utils import logger_util

logger_util.setup_logging()
logger = logger_util.get_logger("userLogger")

gitlog_insights_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
reports_dir = os.path.join(gitlog_insights_dir, 'reports')
html_report_path = os.path.join(reports_dir, 'merge_activity_report.html')

def get_inputs():
    """
    Prompts the user to enter a start date, end date and repository path,
    and validates the inputs.

    Returns: A tuple containing the start date, end date and repository path
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
    except (FileNotFoundError, PermissionError) as report_error:
        logger.error("An error occurred while writing the HTML report: %s", report_error)
        sys.exit(1)



if __name__ == "__main__":
    start_date, end_date, repo_path = get_inputs()
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    try:
        github_api = PRDataExtractor(repo_path)
        merge_details = github_api.get_merged_pr_details(start_date,end_date)
    except PRDataExtractionError as error:
        error_message = f"Error extracting review details for repository '{repo_path}' between {start_date} and {end_date}: {error}"
        logger.error(error_message)
        sys.exit(1)
    if merge_details.empty:
        print(f"No data found betweent the specified dates : {start_date} and {end_date}")
    else:
        weekly_report = get_merge_activity_details(merge_details)
        write_html_report(weekly_report, html_report_path)
        