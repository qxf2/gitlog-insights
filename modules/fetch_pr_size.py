"""
This script fetches the size of the PR in a GitHub repository based on
start_date, end_date, repo

"""
import pandas as pd
import re
from pydriller import Repository

def inference_pr_size(insertions, deletions):
    total_changes = insertions + deletions
    if total_changes < 100:
        return "small"
    elif total_changes < 500:
        return "medium"
    else:
        return "large"

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
                    pr_size = inference_pr_size(pr_insertions,pr_deletions)
                    totalsize = pr_insertions + pr_deletions

                size_of_the_pr[pr_number] = {'PR Number':pr_number,'Insertions': pr_insertions, 'Deletions': pr_deletions,'Size of PR': pr_size}
                # Provide insights based on PR size
                if pr_size == "small":
                    print(f'Insight: This is a small PR ({totalsize}) with minimal changes.')
                elif pr_size == "medium":
                    print(f'Insight: This PR ({totalsize}) has a moderate number of changes.')
                else:
                    print(f'Insight: This is a large PR ({totalsize}) with significant changes.')

        # Create a DataFrame from the data
        df = pd.DataFrame(size_of_the_pr).T
        return df
                
    except Exception as error:
        raise error