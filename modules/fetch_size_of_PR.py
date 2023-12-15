""""
This script fetches the merged PR details for a given time period
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.github_pr_data_extractor import PRDataExtractor
import pandas as pd

def get_PR_details(repo_name, start_date, end_date):
    """
    Gets the PR review details
    """

    try:
        github_api = PRDataExtractor(repo_name)
        pr_details = github_api.get_pr_files_details(start_date, end_date)              
        if pr_details.empty:
            return pd.DataFrame() 
        grouped_pr_details = pr_details.groupby('pr_number').agg({
            'filename': 'nunique',  # Number of unique files changed
            'changes': 'sum'        # Total number of lines changed
        }).reset_index()          
        
        grouped_pr_details.columns = ['pr_number', 'num_files_changed', 'total_lines_changed']

        pr_sizes = pr_details.groupby('pr_number')[['additions', 'deletions']].sum().sum(axis=1)

        print("Size of each pull request:")
        print(pr_sizes)           
        
        return pr_sizes
        
    except Exception as error:
        print(f"An error occurred: {error}")
        return pd.DataFrame()