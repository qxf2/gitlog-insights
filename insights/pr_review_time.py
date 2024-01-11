"""
This script is used to produce the following insight:
Find the average PR review time within the specified time period

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

Note:
To run this script, you would need GitHub Token. For more details, please check Readme.
"""

import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import logger_util
from modules import fetch_pr_review_time
from helpers import github_pr_data_extractor

logger_util.setup_logging()
logger = logger_util.get_logger("userLogger")

gitlog_insights_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
reports_dir = os.path.join(gitlog_insights_dir, 'reports')
html_report_path = os.path.join(reports_dir, 'pr_review_time_report.html')

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
            print("Invalid start date format. Please enter a valid date in YYYY-MM-DD format.")

    while True:
        try:
            end_date_input = input("Enter the end date (YYYY-MM-DD): ")
            end_date_input = datetime.strptime(end_date_input, "%Y-%m-%d")
            if end_date_input > start_date_input:
                break
            print("End date must be greater than start date. Please try again.")

        except ValueError:
            print("Invalid date format. Please try again.")

    start_date_input = start_date_input.strftime("%Y-%m-%d")
    end_date_input = end_date_input.strftime("%Y-%m-%d")
    repo_name = input("Enter the repository name: ")

    return start_date_input, end_date_input, repo_name


def write_html_report(file_info_df, review_time, file_name):
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
        with open(file_name, "w+", encoding="utf-8") as file:
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
    input_start_date, input_end_date, input_repo_name = get_inputs()
    try:
        review_details = fetch_pr_review_time.calculate_review_time(
            input_repo_name, input_start_date, input_end_date
        )
    except github_pr_data_extractor.PRDataExtractionError as error:
        error_message = f"Error extracting review details for repository \
            '{input_repo_name}' between {input_start_date} and {input_end_date}: {error}"
        logger.error(error_message)
        sys.exit(1)
    if not review_details.empty:
        average_review_time = fetch_pr_review_time.compute_inference(
            review_details
        )
        write_html_report(
            review_details,
            average_review_time,
            html_report_path,
        )
        print('\nDetailed report can be found in pr_review_time_report.html\n')
