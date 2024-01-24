""""
This script fetches the PR details for a given time period
"""
import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.github_pr_data_extractor import PRDataExtractor, PRDataExtractionError
from utils import logger_util

logger = logger_util.get_logger("root")


def get_pr_details(repo_name, start_date, end_date):
    """
    Gets the PR review details
    """

    try:
        github_api = PRDataExtractor(repo_name)
        pr_details = github_api.get_pr_files_details(start_date, end_date)
        if pr_details.empty:
            print(
                f"No data found betweent the specified dates : {start_date} and {end_date}"
            )
            return pd.DataFrame([])
        grouped_pr_details = (
            pr_details.groupby("pr_number")
            .agg(
                {
                    "filename": "nunique",  # Number of unique files changed
                    "changes": "sum",  # Total number of lines changed
                }
            )
            .reset_index()
        )
        grouped_pr_details.columns = [
            "pr_number",
            "num_files_changed",
            "total_lines_changed",
        ]
        return grouped_pr_details

    except ValueError as value_error:
        logger.exception("An error occured while extracting PR data %s", value_error)
        raise PRDataExtractionError("Error while extracting PR data") from value_error
    except KeyError as key_error:
        logger.exception("An error occured while extracting PR data %s", key_error)
        raise PRDataExtractionError("Error while extracting PR data") from key_error
    except PRDataExtractionError as error:
        logger.exception("An error occured while extracting PR data %s", error)
        raise PRDataExtractionError("Error while extracting PR data") from error

def get_pr_insights(pr_details):
    "PR insights"
    number_of_lines_changed = pr_details.loc[pr_details["total_lines_changed"].idxmax()]
    pr_number = number_of_lines_changed["pr_number"]
    total_lines_changed = number_of_lines_changed["total_lines_changed"]

    # Framing inferences
    lines_message = (
        f"\n -> The PR#{pr_number} has maximum number of code lines changed: "
        f"{total_lines_changed} lines."
    )
    print("\nInsights for the time period:")
    print(lines_message)

    number_of_files_changed = pr_details.loc[pr_details["num_files_changed"].idxmax()]
    pr_number_files = number_of_files_changed["pr_number"]
    num_files_changed = number_of_files_changed["num_files_changed"]

    files_message = (
        f"\n -> The PR#{pr_number_files} has maximum number of files changed: "
        f"{num_files_changed} changes."
    )
    print(files_message)
