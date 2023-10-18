"""
This script fetches the size of the PR in a GitHub repository based on
start_date, end_date, repo

"""
import pandas as pd
import re
from pydriller import Repository

def find_pr_size(
    repo_path: str,
    start_date: str,
    end_date: str,
):
    """
    Find the PR size in a repository based on the number of commits.

    Args:
        repo_path (str): The path to the repository.
        start_date (str): The start date for filtering commits.
        end_date (str): The end date for filtering commits.

    Returns:
        dataframe: A dataframe containing the file info.
    """
    size_of_the_pr={}

    try:
        for commit in Repository(repo_path, since=start_date, to=end_date).traverse_commits():
            match = re.search(r'#(\d+)', commit.msg)
            if match:
                pr_number = int(match.group(1))
                if pr_number is not None:
                    pr_insertions = commit.insertions
                    pr_deletions = commit.deletions
                    pr_size = pr_insertions + pr_deletions

                size_of_the_pr[pr_number] = {'PR Number':pr_number,'Insertions': pr_insertions, 'Deletions': pr_deletions,'Size of PR': pr_size}

                  
        # Create a DataFrame from the data
        df = pd.DataFrame(size_of_the_pr).T
        return df
                
    except Exception as error:
        raise error