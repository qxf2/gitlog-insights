"""
This script is used to retrieve contributor information for modified files 
in a Git repository within a specified date range.
"""
import sys
import os
from datetime import datetime
from pydriller import Repository
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import logger_util

logger = logger_util.get_logger('root')

class FetchDataError(Exception):
    "To raise exceptions generated while trying to fetch Author data"
    def __init__(self, message):
        super().__init__(message)

def get_contributors_info(repo_path, start_date, end_date):
    """
    Fetches the contributors' information for a given repository within a specific date range.
    Args:
        repo_path (str): The path to the repository to be analyzed.
        start_date (str): The start date of the analysis in the format 'YYYY-MM-DD'.
        end_date (str): The end date of the analysis in the format 'YYYY-MM-DD'.

    Returns:
        pandas.DataFrame: A DataFrame that contains the contributors' information
    """
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        authors_dict = {}

        modifications_dict = {}

        for commit in Repository(repo_path, since=start_date, to=end_date).traverse_commits():
            for modified_file in commit.modified_files:
                file_name = modified_file.filename
                if modified_file.filename not in authors_dict:
                    authors_dict[modified_file.filename] = set()
                authors_dict[modified_file.filename].add(commit.author.name)

                if file_name not in modifications_dict:
                    modifications_dict[file_name] = 0
                modifications_dict[file_name] += \
                    modified_file.added_lines + \
                    modified_file.deleted_lines


        contributors_dict = {}
        for file, authors in authors_dict.items():
            modifications = modifications_dict[file]
            contributors_dict[file] = {
                'File Name': file,
                'Authors': ', '.join(authors),
                'No of Authors': len(authors),
                'Modifications' : modifications
            }
        contributors_df = pd.DataFrame.from_dict(contributors_dict, orient='index')
        return contributors_df

    except ValueError as value_error:
        logger.exception("Error while fetching data %s", value_error)
        raise FetchDataError("Error while fetching data:") from value_error
    except KeyError as key_error:
        logger.exception("Error while fetching data %s", key_error)
        raise FetchDataError("Error while fetching data:") from key_error

