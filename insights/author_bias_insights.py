"""
This script is used to produce the following insight:
Find the all modified files in a GitHub repository within the specified time period along with author details.
This info can help testing teams align their testing efforts accordingly.

Usage:
python author_bias_insights.py

Provide the following inputs:
Enter the start date in YYYY-MM-DD format (eg: 2023-02-01)
Enter the end date in YYYY-MM-DD format (must be greater than start date) (eg: 2023-02-08)
Enter the repository path: local or remote GitHub repositories
(eg: https://github.com/qxf2/newsletter_automation.git)

- The script prompts for necessary inputs and
then fetches the all modified files within the specified date range along with the author names and major(number of authors).
It displays the results in the form of a simple html page.

Outputs:
Provides all modified files from the repository within the specified time period along with author details.
"""

import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import fetch_author_count


def get_inputs():
    """
    Prompts the user to enter a start date, end date, repository path.

    Returns: A tuple containing the start date, end date, repository path.
    """

    while True:
        try:
            start_date_input = input("Enter the start date (YYYY-MM-DD): ")
            break
        except ValueError:
            print(
                "Invalid start date format. Please enter a valid date in YYYY-MM-DD format."
            )

    while True:
        try:
            end_date_input = input("Enter the end date (YYYY-MM-DD): ")
            if end_date_input > start_date_input:
                break
            print("End date must be greater than start date. Please try again.")
        except ValueError:
            print("Invalid date format. Please try again.")

    repo_path_input = input("Enter the repository path (For example:https://github.com/qxf2/qxf2-page-object-model.git): ")

    return start_date_input, end_date_input, repo_path_input


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
    contributors_data = fetch_author_count.get_contributors_info(
        repo_path, start_date, end_date
    )
    write_html_report(contributors_data, "report.html")
