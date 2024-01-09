"""
This script is used to produce the following insight:
Find the size of the PR and number of files changed in a GitHub repository 
within the specified time period.
This info can help testing teams align their testing efforts accordingly.

Usage:
python size_of_PRs.py

Provide the following inputs:
Enter the start date in YYYY-MM-DD format (eg: 2023-02-01)
Enter the end date in YYYY-MM-DD format (must be greater than start date) (eg: 2023-02-08)
Enter the repository path: local or remote GitHub repositories
(eg: https://github.com/qxf2/newsletter_automation.git)

- The script prompts for necessary inputs and
then fetches the max size of the PR and max files changed  within the specified date range.
It displays the results in the form of a simple html page.

Outputs:
The max PR size and Max files modified in the repository based on the number of modifications.
"""

import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import fetch_size_of_pr

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import github_pr_data_extractor

from utils import logger_util
logger_util.setup_logging()
logger = logger_util.get_logger("userLogger")

gitlog_insights_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

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

def write_html_report(file_info_df,file_name):
    """
    Writes the DataFrame to HTML report file.

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
                text = "The best practice is to have 200-400 LOC per PR."
                text += " This extensive change might pose challenges in review and testing"
                file.write(text)
    except (FileNotFoundError, PermissionError) as err:
        print(f"An error occurred while writing the HTML report: {str(err)}")

if __name__ == "__main__":
    start_date, end_date, repo_path = get_inputs()
    try:
        pr_details = fetch_size_of_pr.get_pr_details(repo_path,start_date,end_date)
    except github_pr_data_extractor.PRDataExtractionError as error:
        error_message = f"Error extracting PR details for repository \
            '{repo_path}' between {start_date} and {end_date}: {error}"
        logger.error(error_message)
        sys.exit(1)
    if not pr_details.empty:
        combined_df = fetch_size_of_pr.get_pr_insights(pr_details)
        write_html_report(combined_df, "insights_for_size_of_pr.html")
        print('\nDetailed log analysis can be found in insights_for_size_of_pr.html\n')
