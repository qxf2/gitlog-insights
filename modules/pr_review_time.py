""""
This script fetches the PR review time of all closed PR's for a given time period
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.github_pr_data_extractor import PRDataExtractor
import pandas as pd
from datetime import datetime

def calculate_review_time(repo_name, start_date, end_date):
    """
    Gets the PR review details and calculates the total review time for each PR.
    It also computes the average review time for the given time period
    """

    github_api = PRDataExtractor(repo_name)
    pr_details = github_api.get_pr_details(start_date, end_date)

    pr_details['created_at'] = pd.to_datetime(pr_details['created_at'],errors='coerce')
    pr_details['closed_at'] = pd.to_datetime(pr_details['closed_at'],errors='coerce')
    pr_details = pr_details[pr_details['status'] == 'closed']

    pr_details['review_time'] = pr_details['closed_at'] - pr_details['created_at']

    return pr_details