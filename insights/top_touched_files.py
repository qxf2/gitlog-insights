"""
This script is used to produce the following insight:
Find the most modified files in a GitHub repository within the specified time period
This info can help testing teams align their testing efforts accordingly.

Usage:
python top_touched_files.py

Provide the following inputs:
Enter the start date in YYYY-MM-DD format (eg: 2023-02-01)
Enter the end date in YYYY-MM-DD format (must be greater than start date) (eg: 2023-02-08)
Enter the repository path: local or remote GitHub repositories
(eg: https://github.com/qxf2/newsletter_automation.git)
Optionally, enter the branch name (default is main)
Optionally, enter the file type extension,
(starting with a period) or leave it empty for all file types.

- The script prompts for necessary inputs and
then fetches the most modified files within the specified date range.
It displays the results in the form of a simple html page.

Outputs:
The top files in the repository based on the number of modifications.
"""

import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import fetch_most_modified_files


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
    while True:
        repo_path_input = input("Enter the repository path: ")
        if repo_path_input:
            break
        else:
            print("\nRepo path cannot be empty! Please enter valid repo path(example:https://github.com/qxf2/qxf2-page-object-model)\n")

    branch_input = input("Enter the branch name (default: main): ") or "main"

    file_type_input = input(
        "Enter the file type extention (starting with .) (default: all): "
    )
    if file_type_input == "all":
        file_type_input = ""
    elif not file_type_input.startswith("."):
        print("Defaulting to all files.")
        file_type_input = ""
    else:
        file_type_input = file_type_input.lower()

    return start_date_input, end_date_input, repo_path_input, branch_input, file_type_input


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
    start_date, end_date, repo_path, branch, file_type = get_inputs()
    top_files_df = fetch_most_modified_files.find_top_files(
        repo_path, start_date, end_date, file_type, branch
    )
    write_html_report(top_files_df, "report.html")
