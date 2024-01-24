"""
This script is used to produce the following insight:
Find the files that have high Author Bias during the time period

Usage:
python author_bias_insights.py

Provide the following inputs:
Enter the start date in YYYY-MM-DD format (eg: 2023-02-01)
Enter the end date in YYYY-MM-DD format (must be greater than start date) (eg: 2023-02-08)
Enter the repository path: local or remote GitHub repositories
(eg: https://github.com/qxf2/newsletter_automation.git)

- The script prompts for necessary inputs and then fetches the all modified files within 
the specified date range along with the author names, major(number of authors) and author bias.
It displays the results in the form of a simple html page.

Outputs:
Provides list of files from the repository within the specified 
that have high Author Bias.
"""

import os
import sys
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import fetch_author_count
from utils import logger_util

logger_util.setup_logging()
logger = logger_util.get_logger("userLogger")

gitlog_insights_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
reports_dir = os.path.join(gitlog_insights_dir, "reports")
html_report_path = os.path.join(reports_dir, "report_author_bias.html")


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

    repo_path_input = input(
        "Enter the repository path (For example: "
        "https://github.com/qxf2/qxf2-page-object-model.git ):"
    )

    return start_date_input, end_date_input, repo_path_input


def calculate_author_bias(info_df):
    """
    Calculate the author bias for a given DataFrame.

    Args:
        df (DataFrame): The DataFrame containing the author information, 
        including the number of modifications made by each author.

    Returns:
        DataFrame: The DataFrame containing the top 5 authors with the highest bias, 
        sorted by entropy and number of modifications.

    """
    info_df["Proportion"] = info_df["Modifications"] / info_df["Modifications"].sum()

    # Add a small positive value to avoid zero values in Proportion
    info_df["Proportion"] = info_df["Proportion"] + 0.0001
    info_df["Entropy"] = -info_df["Proportion"] * np.log2(info_df["Proportion"])

    mean_entropy = info_df["Entropy"].mean()
    high_bias_df = info_df[info_df["Entropy"] < mean_entropy]

    sorted_high_bias_df = high_bias_df.sort_values(
        by=["Entropy", "Modifications"], ascending=[True, False]
    ).head(5)

    return sorted_high_bias_df


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
        with open(file_name, "w", encoding="utf-8") as file:
            if file_info_df.empty:
                message = "No data available between the specified dates."
                file.write(message)
            else:
                html = file_info_df.to_html(index=False)
                file.write(html)
    except (FileNotFoundError, PermissionError) as report_error:
        logger.error(
            "An error occurred while writing the HTML report: %s", report_error)
        sys.exit(1)


if __name__ == "__main__":
    start_date, end_date, repo_path = get_inputs()
    try:
        contributors_data = fetch_author_count.get_contributors_info(
            repo_path, start_date, end_date
        )
        report_data = contributors_data.copy()
    except fetch_author_count.FetchDataError as error:
        error_message = f"Error extracting review details for repository \
            '{repo_path}' between {start_date} and {end_date}: {error}"
        logger.error(error_message)
        sys.exit(1)

    if contributors_data.size == 0:
        print("No commits has been done during this time range")
    else:
        high_bias_data = calculate_author_bias(contributors_data)
        num_rows = len(high_bias_data.index)
        if num_rows == 0:
            print("No files have high Author Bias in this repository.")
        elif num_rows < 2:
            print("Not enough data is available to list the files with high Author Bias.")
        else:
            file_list = high_bias_data["File Name"].tolist()
            print("\n Files with High Author Bias during the time period:\n")
            for each_file in file_list:
                print(" -> " + each_file)

        write_html_report(report_data, html_report_path)
        print("\nDetailed report can be found in report_author_bias.html\n")
