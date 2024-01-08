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

        #print (grouped_pr_details)

        #pr_sizes = pr_details.groupby('pr_number')[['additions', 'deletions']].sum().sum(axis=1)

        print("Size of each pull request:")
        #print(pr_sizes)           
        
        return grouped_pr_details
        
    except Exception as error:
        print(f"An error occurred: {error}")
        return pd.DataFrame()
    

def get_PR_insights(pr_details):
    "PR insights"
    number_of_lines_changed = pr_details.loc[pr_details['total_lines_changed'].idxmax()]
      # Creating DataFrames
    lines_changed_df = pd.DataFrame({
        "PR_Number": [number_of_lines_changed['pr_number']],
        "Total_Lines_Changed": [number_of_lines_changed['total_lines_changed']]
    })    
    # Framing inferences
    print(f"\nInsights for PR :")
    print(f"\n -> The PR#{number_of_lines_changed['pr_number']} has maximum number of code lines changed: {number_of_lines_changed['total_lines_changed']} lines. \nThis extensive change might pose challenges in review and testing.")
     
    number_of_files_changed = pr_details.loc[pr_details['num_files_changed'].idxmax()]
    files_changed_df = pd.DataFrame({
        "PR_Number": [number_of_files_changed['pr_number']],
        "Num_Files_Changed": [number_of_files_changed['num_files_changed']]
    })
    print (f"\n -> The PR#{number_of_files_changed['pr_number']} has maximum number of files changed: {number_of_files_changed['num_files_changed']} changes.\n This needs more attention towards review and testing")
    
    # Merging DataFrames
    combined_df = pd.merge(lines_changed_df, files_changed_df, on='PR_Number', how='outer')

    return combined_df

