"""
This script fetches the most modified files in a GitHub repository based on
start_date, end_date, repo, branch, file_type

"""
import sys
import os
from typing import Optional
import heapq
from collections import defaultdict
import pandas as pd
from pydriller import Repository
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import logger_util

logger = logger_util.get_logger("root")


class PyDrillerError(Exception):
    "To catch exceptions raised when accessing PyDriller methods"

def find_top_files(
    repo_path: str,
    start_date: str,
    end_date: str,
    file_type: Optional[str],
    branch: str,
    num_files: int = 5,
):
    """
    Find the top files in a repository based on the number of modifications.

    Args:
        repo_path (str): The path to the repository.
        start_date (str): The start date for filtering commits.
        end_date (str): The end date for filtering commits.
        branch (str): The branch to consider for commits.
        file_type (str, optional): The file type to filter. Defaults to None.

    Returns:
        DataFrame: A dataframe containing the file info.
    """

    file_count = defaultdict(int)
    file_info = defaultdict(
        lambda: {"authors": set(), "messages": [], "dates": [], "complexity": None}
    )
    insights = []
    commit_list = Repository(
        repo_path, since=start_date, to=end_date, only_in_branch=branch
    ).traverse_commits()

    try:
        for commit in commit_list:
            for file in commit.modified_files:
                file_name = file.filename
                if not file_type or file_name.endswith(file_type):
                    file_info[file_name]["authors"].add(commit.author.name)
                    if commit.committer_date is not None:
                        date_str = commit.committer_date.strftime("%Y-%m-%d %H:%M:%S")
                        file_info[file_name]["dates"].append(date_str)
                    file_info[file_name]["messages"].append(commit.msg)
                    file_info[file_name]["complexity"] = (
                        file.complexity if not pd.isna(file.complexity) else -1
                    )
                    file_count[file_name] += 1
    except KeyError as key_error:
        logger.exception(f"KeyError occurred while extracting data : {key_error}")
        raise PyDrillerError(f"An error occurred while extracting data. KeyError: {key_error}")

    pd.set_option("display.max_column", None)

    top_files = heapq.nlargest(num_files, file_count.items(), key=lambda x: x[1])
    data = []

    for file, count in top_files:
        file_dict = {
            "File": file,
            "Count": count,
            "Complexity": file_info[file]["complexity"],
            "Authors": ", ".join(file_info[file]["authors"]),
            "Last Commit Message": file_info[file]["messages"][-1],
            "Last Commit Date": file_info[file]["dates"][-1],
        }
        data.append(file_dict)

    file_info_df = pd.DataFrame(data)
    insights = get_insights(file_info_df, start_date, end_date)
    return file_info_df, insights


def get_insights(
    file_info_df: pd.DataFrame,
    start_date: str,
    end_date: str
):
    """
    Extract and return inferences from the top touched files data

    Args:
        files_info_df : DataFrame containing top touched files data
        start_date : Start date for log data analysis
        end_date : End date for log data analysis

    Returns:
        insights: String containing the inferences
    """
   # Find the file with the highest complexity among the top modified files
    max_complexity_file = file_info_df.loc[file_info_df['Complexity'].idxmax()]['File']
    max_complexity_value = file_info_df['Complexity'].max()
    complexity_summary = f"One of the top modified files having a high complexity of {max_complexity_value} is: {max_complexity_file} "

    # Find the file(s) with the maximum commits
    max_changes_count = file_info_df['Count'].max()
    max_changed_files = file_info_df.loc[(file_info_df['Count']==max_changes_count), 'File'].to_list()
    max_commits_summary = f"The file(s) that had maximum commits (precisely {max_changes_count}) are: {max_changed_files}"

    # Find the author(s) who made the commits to the maximum modified file(s)
    max_commits_authors = file_info_df.loc[(file_info_df['Count']==max_changes_count), 'Authors'].to_list()
    # Removing duplicate author names
    names_lists = [author_names.split(', ') for author_names in max_commits_authors]
    author_names = [name for names_list in names_lists for name in names_list]
    max_commits_authors = list(dict.fromkeys(author_names))
    max_commits_authors_summary = f"Author(s) who made these {max_changes_count} commits are: {max_commits_authors}"

    # Framing inferences
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    insights = f"\nInsights for the duration {start_date_str} to {end_date_str}:\n\n" + "  -> "
    insights = insights + complexity_summary +  "\n  -> " + max_commits_summary +  "\n  -> " + max_commits_authors_summary

    return insights
