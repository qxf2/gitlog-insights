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
        #print (pr_details['pr_number']) 
        for pr_number in pr_details['pr_number']:
            pr_detail_items = github_api.extract_files_data(pr_number)
            print (pr_detail_items)    
        """    
        pr_details['files_changed'] = pr_details.groupby('pr_number')['filename'].nunique()
        print("Number of files changed per pull request:")
        print(pr_details.groupby('pr_number')['files_changed'].nunique())
            
        
        return pr_details
        """
    except Exception as error:
        print(f"An error occurred: {error}")
        return pd.DataFrame()