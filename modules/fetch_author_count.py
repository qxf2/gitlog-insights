"""
This script is used to retrieve contributor information for modified files 
in a Git repository within a specified date range.
"""
from datetime import datetime
from pydriller import Repository
import pandas as pd

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

        for commit in Repository(repo_path, since=start_date, to=end_date).traverse_commits():
            for modified_file in commit.modified_files:
                if modified_file.filename not in authors_dict:
                    authors_dict[modified_file.filename] = set()
                authors_dict[modified_file.filename].add(commit.author.name)

        contributors_dict = {}
        for file, authors in authors_dict.items():
            contributors_dict[file] = {
                'File Name': file,
                'Authors': ', '.join(authors),
                'Major': len(authors)
            }

        contributors_df = pd.DataFrame.from_dict(contributors_dict, orient='index')
        return contributors_df

    except ValueError as error:
        print(f"An error occurred: {str(error)}")
        return None
    